import pytest
from aiohttp import ClientResponseError, ClientSession

from async_roadtechs_downloader import authenticate
from exceptions import AlreadyLoggedInError


@pytest.mark.asyncio
async def test_authenticate() -> None:

    async with ClientSession() as session:
        result = await authenticate(session, "https://www.roadtechs.com/bbclient/login.php", "", "")
        assert result.status == 200

        # await session.post("https://www.roadtechs.com/bbclient/logout.php")

@pytest.mark.asyncio
async def test_authenticate_logged_in() -> None:

    with pytest.raises(AlreadyLoggedInError):
        async with ClientSession() as session:
            await authenticate(session, "https://www.roadtechs.com/bbclient/login.php", "", "")

            await session.post("https://www.roadtechs.com/bbclient/logout.php")

@pytest.mark.asyncio
async def test_authenticate_bad_request() -> None:

    with pytest.raises(ClientResponseError):
        async with ClientSession(raise_for_status=True) as session:
            await authenticate(session, "https://www.roadtechs.com/bbclient/loginurl.php", "test", "test")

            await session.post("https://www.roadtechs.com/bbclient/logout.php")
