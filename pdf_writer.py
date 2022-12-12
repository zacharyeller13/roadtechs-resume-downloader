import pdfkit
from bs4 import BeautifulSoup


def get_resume_name(soup: BeautifulSoup) -> str:

    tag = soup.find("span", id="hdr1")
    name = tag.text.replace('\n', '').split() if tag else []

    return ' '.join(name)

def write_pdf(soup: BeautifulSoup) -> bool:

    resume_name = get_resume_name(soup)
    print(resume_name)

    if resume_name != "":
        return pdfkit.from_string(str(soup.body), f"{resume_name}.pdf")
    else:
        return False
