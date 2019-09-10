import pytest

from DNA_analyser_IBP.callers.user_caller import User


from . import vcr_instance


@pytest.fixture(scope="module")
@vcr_instance.use_cassette
def host():
    return User(email="host", password="host", server="http://localhost:8080/api")


@pytest.fixture(scope="module")
@vcr_instance.use_cassette
def user():
    return User(
        email="user@mendelu.cz", password="user", server="http://localhost:8080/api"
    )


def test_user_creation(user):
    """It should create user and test it's features."""
    assert isinstance(user.id, str)
    assert isinstance(user.jwt, str)
    assert user.id == "6afdeb76-a6ee-4d0b-b07a-0cc0ee9ba885"


def test_host_creation(host):
    """It should create host user and test it's features."""
    assert isinstance(host.id, str)
    assert isinstance(host.jwt, str)
    assert host.email == "host"
    assert host._password == "host"


def test_not_existing_user():
    """It should test not logged user."""
    with pytest.raises(Exception):
        User(email="example@exampl.cz", password="example")
