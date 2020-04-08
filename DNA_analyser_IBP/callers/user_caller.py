# user_caller.py
# !/usr/bin/env python3


import jwt
import json
import requests

from DNA_analyser_IBP.utils import validate_email, validate_text_response, exception_handler, Logger


class User:
    """User class providing information for current user"""

    @exception_handler
    def __init__(self, email: str, password: str, server: str):
        """
        Init and autologin user

        Args:
            email (str): user email
            password (str): user password
            server (str): api server address [Default=http://bioinformatics.ibp.cz:8888/api]
        """
        if email == "host" or validate_email(email):
            self.server = server  # api address
            self.email = email  # tested email
            self._password = password  # user password
            # params obtained by server
            self.jwt, self.id, self.expire_at = self._sign_in()  # /api/jwt
            # if obtained then success print
            Logger.info(f"User {self.email} logged in!")
        else:
            Logger.error(f"Wrong email format!")

    def __str__(self):
        return f"User {self.id}"

    def __repr__(self):
        return f"<User {self.id}>"

    @exception_handler
    def _sign_in(self) -> tuple:
        """
        Sign in at http://bioinformatics.ibp.cz:8888/api

        Returns:
            tuple: JWT string, user id, expiration date
        """
        header = {"Content-type": "application/json", "Accept": "text/plain"}

        if self.email != "host":
            response: object = requests.put(
                f"{self.server}/jwt",
                data=json.dumps(
                    {"login": self.email, "password": self._password}),
                headers=header,
            )
        else:
            response: object = requests.post(
                f"{self.server}/jwt", headers=header)

        jwt_token: str = validate_text_response(
            response=response, status_code=201)
        # decode jwt token to obtain id and expire date
        data: dict = jwt.decode(jwt_token, verify=False)
        return jwt_token, data["id"], data["exp"]
