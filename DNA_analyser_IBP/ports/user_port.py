# user_port.py

from typing import TYPE_CHECKING

from DNA_analyser_IBP.adapters import UserAdapter

if TYPE_CHECKING:
    from DNA_analyser_IBP.models import User


class UserPort:
    """
    User port
    """

    def __init__(self, user: "User"):
        self.user: "User" = user
        self.adapter: "UserAdapter" = UserAdapter()

    def sign_in(self, user: "User") -> "User":
        return self.adapter.sign_in(user=user)
