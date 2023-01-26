import asyncio
from getpass import getpass

import pdfkit
from aiohttp import ClientResponse, ClientSession
from bs4 import BeautifulSoup

from exceptions import AlreadyLoggedInError, LoginError
from pdf_writer import write_pdf, get_resume_name


def parse_login(soup: BeautifulSoup) -> None:
    """
    Parse HTML of login attempt to raise errors if login fails

    Raises an error or returns None
    """

    def find_error(tag):
        return tag.name=='b' and "Error Logging In:" in tag.parent.contents[0]

    if soup.find_all("input", {"name": "login2", "value": "Force Login"}):
        raise AlreadyLoggedInError("The user is already logged in elsewhere - please close all sessions")

    elif soup.find_all(find_error):
        raise LoginError("Username or password was incorrect. Please retry.")


async def authenticate(session: ClientSession, url: str, username: str, password: str) -> ClientResponse:
    """
    Log into a `ClientSession` for use in async requests,
    raising exception for response other than 200 or if user already logged in

    Return a `ClientResponse` object
    """

    resp = await session.post(url, data={
        "client_name": username,
        "pass1": password,
        "Login": "Login"
    })

    if resp.status == 200:

        soup = BeautifulSoup(await resp.text(), 'html.parser')

        parse_login(soup)

    return resp


async def deauth(session: ClientSession) -> ClientResponse:
    """
    Log out of `ClientSession`
    """

    return await session.post("https://www.roadtechs.com/bbclient/logout.php")


async def validate_resume(profile_response: ClientResponse) -> bool:
    """
    Parse HTML of profile to validate if it is a valid profile/resume

    Return a boolean.
    """

    profile = BeautifulSoup(await profile_response.text(), "html.parser")

    def find_error(tag):
        return tag.name=="span" and tag.get('id')=="hdr1" and "Sorry, profile appears to be incomplete." in tag.contents[0]
    
    if profile.find_all(find_error):
        return False

    return True

def get_validation_tasks(responses: list[ClientResponse]) -> list[asyncio.Task]:
    """
    Get all async tasks for validating the returned profiles

    Return a list of `asyncio.Task` objects to be processed later
    """

    tasks = []

    for response in responses:
        tasks.append(asyncio.create_task(validate_resume(response)))

    return tasks


async def get_profile(url: str, session: ClientSession, user_id: int, semaphore: asyncio.Semaphore) -> ClientResponse:
    """
    Get a single profile from /profile_print.php using the passed in `user_id`

    Return the ClientResponse
    """

    data = {
        "userid": f"{user_id}",
        "printable": "Printable+Profile"
    }
    
    async with semaphore:
        response = await session.post(url, data=data)
        return response


def get_profile_tasks(
    url: str, session: ClientSession, end_profile: int, semaphore: asyncio.Semaphore, start_profile: int = 0, 
) -> list[asyncio.Task]:
    """
    Get all async tasks for requesting printable profiles

    Return a list of `asyncio.Task` objects
    """

    tasks = []

    for i in range(start_profile, end_profile):
        tasks.append(asyncio.create_task(get_profile(url, session, i, semaphore)))

    return tasks

def get_resume_count() -> int:
    """
    Request the number of valid resumes from the user

    Return the provided resume_count as an int or fallback to default value if input cannot be converted to int 
    """

    resume_count = input("Input the max number of resumes: ").strip()

    try:
        resume_count = int(resume_count)
    except ValueError:
        print("Valid number not provided, falling back to default value (6978)")
        resume_count = 6978

    return resume_count


async def main() -> None:

    login_url = "https://www.roadtechs.com/bbclient/login.php"
    profile_url = "https://www.roadtechs.com/bbclient/profile_print.php"

    # Prompt user for login information
    username = input("Please type your username: ")
    password = getpass("Please type your password (Output will remain blank as you type for privacy): ")

    # Get the max resume count to be downloaded
    # Number of resumes constantly changes - best to request from the user than to hardcode
    # Could eventually grab it directly from the site
    resume_count = get_resume_count()

    # Set up a semaphore to prevent overloading the server with requests
    semaphore = asyncio.Semaphore(500)

    async with ClientSession() as session:

        # Authenticate the ClientSession with username and password provided above
        response = await authenticate(session, login_url, username, password)
        print(response)

        # Get async tasks and run to retrieve all profiles
        profile_tasks = get_profile_tasks(profile_url, session, resume_count, semaphore)
        responses = await asyncio.gather(*profile_tasks)

        # Get async validation tasks and run to validate profiles
        validation_tasks = get_validation_tasks(responses)
        validations = await asyncio.gather(*validation_tasks)

        # Request and validation loop until valid_count == resume_count
        # Initial set of validations
        valid_count = sum([validation for validation in validations if validation])
        start_profile = resume_count
        end_profile = resume_count + (resume_count - valid_count) + 1
        print(valid_count, start_profile, end_profile)

        # All other validations
        while valid_count != resume_count:
            
            print(f"Valid resumes found: {valid_count}")
            print(f"Fetching profiles {start_profile} through {end_profile}")

            # Get profile tasks and run
            profile_tasks = get_profile_tasks(profile_url, session, end_profile, semaphore, start_profile)
            responses = await asyncio.gather(*profile_tasks)

            # Get validation tasks and run
            validation_tasks = get_validation_tasks(responses)
            validations = await asyncio.gather(*validation_tasks)

            valid_count += sum([validation for validation in validations if validation])
            start_profile = end_profile
            end_profile += (resume_count - valid_count)
            print(valid_count, start_profile, end_profile)

        # Deauthorize and close the session 
        await deauth(session)
        await session.close()


if __name__ == "__main__":

    asyncio.run(main())