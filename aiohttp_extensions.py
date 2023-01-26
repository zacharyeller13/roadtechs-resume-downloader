from aiohttp import ClientResponse, ClientSession
from bs4 import BeautifulSoup

from exceptions import AlreadyLoggedInError, LoginError

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