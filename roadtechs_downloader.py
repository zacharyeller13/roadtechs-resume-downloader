from bs4 import BeautifulSoup, Comment
from requests import Session

def authenticate() -> Session:

    raise NotImplementedError

def get_printable_profile() -> BeautifulSoup:

    raise NotImplementedError

def write_pdf() -> bool:

    raise NotImplementedError

def main() -> None:
    
    raise NotImplementedError

if __name__ == "__main__":

    main()