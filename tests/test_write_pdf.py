import pytest

from pdf_writer import write_pdf


def test_write_pdf() -> None:

    with pytest.raises(NotImplementedError):
        write_pdf()