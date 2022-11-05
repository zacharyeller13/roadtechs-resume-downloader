from roadtechs_downloader import get_printable_profile
import pytest

def test_get_printable_profile() -> None:

    with pytest.raises(NotImplementedError):
        get_printable_profile()
