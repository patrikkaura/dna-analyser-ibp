import pytest

from . import DEV_URL
from DNA_analyser_IBP.callers.user_caller import User


@pytest.fixture(scope="module")
def host():
    return User(email="host", password="host", server=DEV_URL)


@pytest.fixture(scope="module")
def user():
    return User(email="user@mendelu.cz", password="user", server=DEV_URL)


class TestUser:

    def test_user_creation(self, user):
        """It should create user and test it's features."""
        assert isinstance(user.id, str)
        assert isinstance(user.jwt, str)
        assert user.id == "cc599bcd-3099-4897-84eb-cd549da38f41"

    def test_host_creation(self, host):
        """It should create host user and test it's features."""
        assert isinstance(host.id, str)
        assert isinstance(host.jwt, str)
        assert host.email == "host"
        assert host._password == "host"

    def test_not_existing_user(self):
        """It should test not logged user."""
        with pytest.raises(Exception):
            User(email="example@exampl.cz", password="example")
