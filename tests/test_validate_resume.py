import os

import pytest
from bs4 import BeautifulSoup

from async_roadtechs_downloader import validate_resume

with open(f"{os.path.dirname(__file__)}/invalid_profile.html") as f:
    file = f.read()

invalid_profile = BeautifulSoup(file, "html.parser")

with open(f"{os.path.dirname(__file__)}/valid_profile.html") as f:
    file = f.read()

valid_profile = BeautifulSoup(file, "html.parser")

@pytest.mark.asyncio
async def test_validate_resume_bad() -> None:
    """Test the `validate_resume` returns `False` for an invalid profile"""

    assert await validate_resume(invalid_profile) == False

@pytest.mark.asyncio
async def test_validate_resume_valid() -> None:
    """Test that `validate_resume` returns `True` for valid profiles"""

    assert await validate_resume(valid_profile) == True