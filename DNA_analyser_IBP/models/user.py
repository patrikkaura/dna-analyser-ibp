# user.py


class User:
    """
    User model object
    """

    def __init__(self, email: str, password: str, server: str) -> None:
        self.id: str = None
        self.jwt: str = None
        self.email: str = email
        self.server: str = server
        self.password: str = password
        self.is_logged_in: bool = False

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
