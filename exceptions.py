class AlreadyLoggedInError(Exception):
    """
    User is already logged in and must be logged out to proceed
    """

class LoginError(Exception):
    """
    Username or password was incorrect and login has failed
    """