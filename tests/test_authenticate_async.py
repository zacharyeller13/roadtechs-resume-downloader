import pytest
from aiohttp import ClientResponseError, ClientSession

from async_roadtechs_downloader import authenticate, deauth
from exceptions import AlreadyLoggedInError, LoginError


@pytest.mark.asyncio
async def test_authenticate() -> None:

    async with ClientSession() as session:
        result = await authenticate(session, "https://www.roadtechs.com/bbclient/login.php", "", "")
        assert result.status == 200

@pytest.mark.asyncio
async def test_authenticate_logged_in() -> None:

    with pytest.raises(AlreadyLoggedInError):
        async with ClientSession() as session:
            await authenticate(session, "https://www.roadtechs.com/bbclient/login.php", "", "")

            await session.post("https://www.roadtechs.com/bbclient/logout.php")

@pytest.mark.asyncio
async def test_authenticate_bad_url() -> None:

    with pytest.raises(ClientResponseError):
        async with ClientSession(raise_for_status=True) as session:
            await authenticate(session, "https://www.roadtechs.com/bbclient/loginurl.php", "test", "test")

@pytest.mark.asyncio
async def test_authenticate_bad_login() -> None:

    with pytest.raises(LoginError):
        async with ClientSession() as session:
            await authenticate(session, "https://www.roadtechs.com/bbclient/login.php", "test", "test")

@pytest.mark.asyncio
async def test_deauth() -> None:

    async with ClientSession() as session:
        result = await deauth(session)
        assert result.status == 200
