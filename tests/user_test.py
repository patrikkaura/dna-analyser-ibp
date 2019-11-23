import pytest

from . import DEV_URL
from DNA_analyser_IBP.callers.user_caller import User


@pytest.fixture(scope="module")
def host():
    return User(email="host", password="host", server=DEV_URL)


@pytest.fixture(scope="module")
def user():
    return User(email="test@python.cz", password="test", server=DEV_URL)


class TestUser:

    def test_user_creation(self, user):
        """It should create user and test it's features."""
        assert isinstance(user.id, str)
        assert isinstance(user.jwt, str)
        assert user.id == "2a1d8c92-4b7e-4b37-b703-7abde3308d2b"

    def test_host_creation(self, host):
        """It should create host user and test it's features."""
        assert isinstance(host.id, str)
        assert isinstance(host.jwt, str)
        assert host.email == "host"
        assert host._password == "host"
