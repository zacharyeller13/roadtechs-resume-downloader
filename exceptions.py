from aiohttp import ClientError


class AlreadyLoggedInError(ClientError):
    """
    User is already logged in and must be logged out to proceed
    """