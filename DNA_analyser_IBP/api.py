# api.py
# !/usr/bin/env python3
"""
Module with API object for manipulation with BPI REST API.
"""
from getpass import getpass

from .singleton import Singleton
from .callers import User
from .interfaces import G4Hunter, Sequence, G4Killer, P53


class Api(metaclass=Singleton):
    """Api class contains all methods for working with BPI REST API."""

    def __init__(self, *, server: str = "http://bioinformatics.ibp.cz:8888/api"):
        """
        Create API object and login
        :param server: URL to ibp bioinformatics server
        """
        # retrieving data from user, default = host accont
        email = input("Enter your email\t") or "host"
        password = getpass("Enter your password\t", stream=None) or "host"
        print(f'User {email} try to login ...')

        self.user = User(email=email, password=password, server=server)
        self.sequence = Sequence(user=self.user)
        self.g4hunter = G4Hunter(user=self.user)
        self.g4killer = G4Killer(user=self.user)
        self.p53 = P53(user=self.user)

    def __repr__(self):
        return f"<Api: {self.user.server} user: {self.user.email}>"

    def __str__(self):
        return f"Api: {self.user.server} user: {self.user.email}"
