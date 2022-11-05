from exceptions import AlreadyLoggedInError
from requests import RequestException, Session
from roadtechs_downloader import authenticate
import pytest

def test_authenticate() -> None:

    assert isinstance(authenticate("https://www.roadtechs.com/bbclient/login.php", "", ""), Session) 

def test_authenticate_logged_in() -> None:

    with pytest.raises(AlreadyLoggedInError):
        authenticate("https://www.roadtechs.com/bbclient/login.php", "", "")

def test_authenticate_bad_request() -> None:

    with pytest.raises(RequestException):
        authenticate("https://www.roadtechs.com/bbclient/loginurl.php", "test", "test")