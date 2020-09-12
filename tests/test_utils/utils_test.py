import pytest

from DNA_analyser_IBP.utils import get_file_name, join_url, validate_email, normalize_name


def test_filename_generator() -> None:
    """It should create new path from original"""

    new_path: str = get_file_name(original_path='/test/test.txt', out_path='/test/test_out', file_format='csv')
    assert new_path == '/test/test_out/test.csv'


@pytest.mark.parametrize(
    "original,normalized",
    [('ds/dsadsa', 'dsdsadsa'), ('ds@', 'ds'), ('ds#', 'ds')],
)
def test_normalize_name(original: str, normalized: str) -> None:
    """It should normalize name"""

    processed: str = normalize_name(name=original)
    assert processed == normalized


@pytest.mark.parametrize(
    "email,result",
    [('test@test.cz', True), ('ds@', False), ('test@test', False)],
)
def test_validate_email(email: str, result: bool) -> None:
    """It should validate emails"""

    assert validate_email(email) is result


def test_join_url() -> None:
    """It should joint url's"""

    url: str = join_url('test', 'test', 'test.csv')
    assert url == 'api/test/test.csv'
