import os
import pdfkit

from aiohttp import ClientResponse
from bs4 import BeautifulSoup


def get_resume_name(soup: BeautifulSoup) -> str:

    tag = soup.find("span", id="hdr1")
    name = tag.text.replace('\n', '').split() if tag else []

    return ' '.join(name)

def write_pdf(soup: BeautifulSoup) -> bool:

    resume_name = get_resume_name(soup)

    if resume_name != "":
        return pdfkit.from_string(str(soup.body), f"{os.path.dirname(__file__)}/resumes/{resume_name}.pdf")
    else:
        return False

async def write_pdfs(responses: list[ClientResponse], validations: list[bool]) -> None:

    for response, is_valid in zip(responses, validations):

        if is_valid:
            write_pdf(BeautifulSoup(await response.text(), "html.parser"))
