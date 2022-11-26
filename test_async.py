import asyncio

import pdfkit
from aiohttp import ClientResponse, ClientSession
from bs4 import BeautifulSoup

from exceptions import AlreadyLoggedInError

login_url = "https://www.roadtechs.com/bbclient/login.php"
login_data = {
    "client_name": "",
    "pass1": "",
    "Login": "Login"
}

profile_url = "https://www.roadtechs.com/bbclient/profile_print.php"


async def authenticate(session: ClientSession, url: str, username: str, password: str) -> ClientResponse:
    """
    Log into a ClientSession for use in async requests,
    raising exception for response other than 200 or if user already logged in

    Return a ClientSession object
    """

    resp = await session.post(url, data={
        "client_name": username,
        "pass1": password,
        "Login": "Login"
    })

    if resp.status == 200:

        soup = BeautifulSoup(await resp.text(), 'html.parser')

        if soup.find_all("input", {"name": "login2", "value": "Force Login"}):

            raise AlreadyLoggedInError("The user is already logged in elsewhere - please close all sessions")

        return resp

def get_tasks(url: str, session: ClientSession) -> list[asyncio.Task]:
    """
    Get all async tasks for requesting printable profiles

    Return a list of asyncio.Task objects
    """

    tasks = []

    for i in [6918]:
        data = {
            "userid": f"{i}",
            "printable": "Printable+Profile"
        }
        tasks.append(asyncio.create_task(session.post(url, data=data)))

    return tasks

async def main(login_url: str, login_data: dict) -> None:
    async with ClientSession() as session:
        response = await authenticate(session, login_url, "", "!")
        print(response)

        # tasks = get_tasks("https://www.roadtechs.com/bbclient/profile_print.php", session)
        # responses = await asyncio.gather(*tasks)
        # for response in responses:
        #     pdfkit.from_string(str(soup.body), "string_body_out.pdf")

        await session.post("https://www.roadtechs.com/bbclient/logout.php")
        await session.close()

if __name__ == "__main__":

    asyncio.run(main(login_url, login_data))