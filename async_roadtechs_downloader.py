import asyncio
from getpass import getpass

import pdfkit
from aiohttp import ClientResponse, ClientSession
from bs4 import BeautifulSoup

from exceptions import AlreadyLoggedInError, LoginError
from pdf_writer import write_pdf


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

def get_tasks(url: str, session: ClientSession) -> list[asyncio.Task]:
    """
    Get all async tasks for requesting printable profiles

    Return a list of `asyncio.Task` objects
    """

    tasks = []

    for i in [6918]:
        data = {
            "userid": f"{i}",
            "printable": "Printable+Profile"
        }
        tasks.append(asyncio.create_task(session.post(url, data=data)))

    return tasks

async def main() -> None:

    login_url = "https://www.roadtechs.com/bbclient/login.php"
    username = input("Please type your username: ")
    password = getpass("Please type your password (Output will remain blank as you type for privacy): ")

    profile_url = "https://www.roadtechs.com/bbclient/profile_print.php"

    async with ClientSession() as session:
        response = await authenticate(session, login_url, username, password)
        print(response)

        tasks = get_tasks("https://www.roadtechs.com/bbclient/profile_print.php", session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            soup = BeautifulSoup(await response.text(), "html.parser")
            # pdfkit.from_string(str(soup.body), "string_body_out.pdf")

        await deauth(session)
        await session.close()

if __name__ == "__main__":

    asyncio.run(main())