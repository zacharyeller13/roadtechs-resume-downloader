import os

import pytest
from bs4 import BeautifulSoup

from pdf_writer import get_resume_name, write_pdf

with open(f"{os.path.dirname(__file__)}/valid_profile.html") as f:
    file = f.read()

soup = BeautifulSoup(file, "html.parser")
bad_soup = BeautifulSoup("", "html.parser")

def test_get_resume_name() -> None:

    assert get_resume_name(soup) == "Testy McTesterson"

def test_get_resume_name_bad() -> None:

    assert get_resume_name(bad_soup) == ""

def test_write_pdf() -> None:

    assert write_pdf(soup) == True

def test_write_pdf_bad() -> None:

    assert write_pdf(bad_soup) == False
