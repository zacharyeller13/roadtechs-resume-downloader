from exceptions import AlreadyLoggedInError
from roadtechs_downloader import authenticate
import pytest

def test_authenticate() -> None:

    with pytest.raises(AlreadyLoggedInError):
        authenticate("test", "test")