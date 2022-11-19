import asyncio

import pdfkit
from aiohttp import ClientResponse, ClientSession
from bs4 import BeautifulSoup

login_url = "https://www.roadtechs.com/bbclient/login.php"
login_data = {
    "client_name": "",
    "pass1": "",
    "Login": "Login"
}

profile_url = "https://www.roadtechs.com/bbclient/profile_print.php"


async def authenticate(session: ClientSession, url: str, username: str, password: str) -> ClientResponse:

    resp = await session.post(url, data={
        "client_name": username,
        "pass1": password,
        "Login": "Login"
    })

    return resp

def get_tasks(url: str, session: ClientSession) -> list:
    tasks = []

    for i in [6918]:
        data = {
            "userid": f"{i}",
            "printable": "Printable+Profile"
        }
        tasks.append(asyncio.create_task(session.post(url, data=data)))

    return tasks

async def main(login_url, login_data):
    async with ClientSession() as session:
        response = await authenticate(session, login_url, "", "")
        # response = await session.post(login_url, data=login_data)
        # print(BeautifulSoup(await response.text(), 'html.parser'))
        tasks = get_tasks("https://www.roadtechs.com/bbclient/profile_print.php", session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            soup = BeautifulSoup(await response.text(), "html.parser")
            pdfkit.from_string(str(soup.body), "string_body_out.pdf")

        await session.post("https://www.roadtechs.com/bbclient/logout.php")
        await session.close()

asyncio.run(main(login_url, login_data))