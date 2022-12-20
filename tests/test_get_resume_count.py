import pytest

from async_roadtechs_downloader import get_resume_count


def test_get_resume_count(monkeypatch) -> None:

    monkeypatch.setattr("builtins.input", lambda _: "12")

    assert get_resume_count() == 12

def test_get_resume_count_fallback(monkeypatch) -> None:

    monkeypatch.setattr("builtins.input", lambda _: "1a")

    assert get_resume_count() == 6978