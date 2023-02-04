import os
import unittest.mock

import pytest

from tasks import validate_resume


@pytest.mark.asyncio
async def test_validate_resume_bad() -> None:
    """Test the `validate_resume` returns `False` for an invalid profile"""

    with open(f"{os.path.dirname(__file__)}/invalid_profile.html") as f:
        invalid_profile = f.read()

    mock_invalid = unittest.mock.AsyncMock()
    mock_invalid.text.return_value = invalid_profile

    assert await validate_resume(mock_invalid) == False

@pytest.mark.asyncio
async def test_validate_resume_valid() -> None:
    """Test that `validate_resume` returns `True` for valid profiles"""

    with open(f"{os.path.dirname(__file__)}/valid_profile.html") as f:
        valid_profile = f.read()

    mock_valid = unittest.mock.AsyncMock()
    mock_valid.text.return_value = valid_profile

    assert await validate_resume(mock_valid) == True