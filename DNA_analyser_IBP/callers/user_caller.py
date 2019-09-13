# user_caller.py
# !/usr/bin/env python3


import jwt
import json
import requests
from datetime import datetime
from typing import Union

from ..utils import validate_email, validate_text_response


class User:
    """User class providing information for current user"""

    def __init__(self, email: str, password: str, server: str):
        """
        Init and autologin user
        :param email: user email
        :param password: user passwod
        :param server: http://bioinformatics.ibp.cz:8888/api
        """
        if email == "host" or validate_email(email):
            self.server = server  # api address
            self.email = email  # tested email
            self._password = password  # user password
            # params obtained by server
            self.jwt, self.id, self.expire_at = self._sign_in()  # /api/jwt
            # if obtained then success print
            print(f"User {self.email} logged in: {datetime.utcnow()}")
        else:
            raise ValueError("Wrong email format.")

    def __str__(self):
        return f"User {self.id}"

    def __repr__(self):
        return f"<User {self.id}>"

    def _sign_in(self) -> Union[tuple, Exception]:
        """
        Sign in at http://bioinformatics.ibp.cz:8888/api
        :return:JWT string, user id, expiration date
        """
        header = {"Content-type": "application/json", "Accept": "text/plain"}

        if self.email != "host":
            response = requests.put(f"{self.server}/jwt", data=json.dumps({"login": self.email, "password": self._password}), headers=header)
        else:
            response = requests.post(f"{self.server}/jwt", headers=header)

        jwt_token = validate_text_response(response=response, status_code=201)
        data = jwt.decode(jwt_token, verify=False)  # decode jwt token to obtain id and expire date
        return jwt_token, data["id"], data["exp"]
