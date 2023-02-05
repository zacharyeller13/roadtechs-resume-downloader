import os
import pdfkit

from aiohttp import ClientResponse
from bs4 import BeautifulSoup


def get_resume_name(soup: BeautifulSoup) -> str:

    tag = soup.find("span", id="hdr1")
    name = tag.text.replace('\n', '').split() if tag else []

    return ' '.join(name)

def write_pdf(soup: BeautifulSoup, destination_folder: str) -> bool:

    resume_name = get_resume_name(soup)

    if resume_name != "":
        return pdfkit.from_string(
            str(soup.body), 
            f"{destination_folder}/{resume_name}.pdf",
            options={'encoding': "UTF-8"}
        )
    else:
        return False

async def write_pdfs(responses: list[ClientResponse], validations: list[bool], destination_folder: str) -> None:
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for response, is_valid in zip(responses, validations):

        if is_valid:
            write_pdf(BeautifulSoup(await response.text(), "html.parser"), destination_folder)
