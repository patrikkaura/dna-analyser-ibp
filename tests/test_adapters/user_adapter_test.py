import re

from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.models import User
from DNA_analyser_IBP.adapters import UserAdapter

JWT_REGEX = re.compile("^[A-Za-z0-9-_=]+.[A-Za-z0-9-_=]+.?[A-Za-z0-9-_.+/=]*$")


class TestUserAdapter:
    def test_user_host_creation(self) -> None:
        """It should create User model and log in"""
        email: str = "host"
        password: str = "host"

        user = UserAdapter.sign_in(
            User(email=email, password=password, server=Config.SERVER_CONFIG.PRODUCTION)
        )

        assert isinstance(user, User)
        assert isinstance(user.jwt, str)
        assert bool(JWT_REGEX.match(user.jwt))

    def test_user_creation(self) -> None:
        """It should create User model for test account"""
        email: str = "user@mendelu.cz"
        password: str = "user"

        user = UserAdapter.sign_in(
            User(email=email, password=password, server=Config.SERVER_CONFIG.PRODUCTION)
        )

        assert isinstance(user, User)
        assert isinstance(user.jwt, str)
        assert bool(JWT_REGEX.match(user.jwt))
