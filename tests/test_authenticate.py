from roadtechs_downloader import authenticate
import pytest

def test_authenticate() -> None:

    with pytest.raises(NotImplementedError):
        authenticate("test", "test")