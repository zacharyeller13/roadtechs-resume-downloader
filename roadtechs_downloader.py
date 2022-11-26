from bs4 import BeautifulSoup, Comment
from requests import RequestException, Session

from exceptions import AlreadyLoggedInError


def authenticate(url: str, username: str, password: str) -> Session:
    """
    Return persistant, logged in Session object for use in requests,
    raising exception for response other than 200 or if user is already logged in elsewhere
    """

    session = Session()

    resp = session.post(url, data={
        "client_name": username,
        "pass1": password,
        "Login": "Login"
    })

    if resp.status_code == 200:

        soup = BeautifulSoup(resp.content, "html.parser")

        if soup.find_all("input", {"name": "login2", "value": "Force Login"}):

            raise AlreadyLoggedInError

        return session

    else:
        raise RequestException(f"Request returned {resp.status_code}")

def get_printable_profile() -> BeautifulSoup:

    raise NotImplementedError

def write_pdf() -> bool:

    raise NotImplementedError

def main() -> None:
    
    raise NotImplementedError

if __name__ == "__main__":

    main()