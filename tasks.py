import asyncio

from aiohttp import ClientResponse, ClientSession
from bs4 import BeautifulSoup

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