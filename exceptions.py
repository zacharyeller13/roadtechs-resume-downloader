from requests import RequestException

class AlreadyLoggedInError(RequestException):
    """
    User is already logged in and must be logged out to proceed
    """