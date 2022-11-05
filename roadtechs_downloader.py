from bs4 import BeautifulSoup, Comment
from requests import Session
from exceptions import AlreadyLoggedInError

def authenticate(username: str, password: str) -> Session:

    raise AlreadyLoggedInError

def get_printable_profile() -> BeautifulSoup:

    raise NotImplementedError

def write_pdf() -> bool:

    raise NotImplementedError

def main() -> None:
    
    raise NotImplementedError

if __name__ == "__main__":

    main()