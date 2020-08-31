# user.py
# !/usr/bin/env python3


class User:
    """
    User model object
    """

    def __init__(self, email: str, password: str, server: str) -> None:
        self.id = None
        self.jwt = None
        self.email = email
        self.server = server
        self.password = password

    def __str__(self):
        return f"UserModel {self.id}"

    def __repr__(self):
        return f"<UserModel {self.id}>"

    def set_login(self, jwt: str, id: str) -> None:
        """
        Set login params

        Args:
            jwt (str): JSON web token
            id (str): user id

        Returns:

        """
        self.id = id
        self.jwt = jwt
