# api.py
# !/usr/bin/env python3
"""
Library with API object for manipulation with BPI REST API.
Available classes:
- Api: object encapsulation whole rest api.
"""
from getpass import getpass

from .callers.user_caller import User

from .interfaces.g4hunter_interface import G4Hunter
from .interfaces.sequence_interface import Sequence
from .interfaces.g4killer_interface import G4Killer
from .interfaces.p53_interface import P53

from .singleton import Singleton


class Api(metaclass=Singleton):
    """Api class contains all methods for working with BPI REST API."""

    def __init__(self, server: str = "http://bioinformatics.ibp.cz:8888/api"):
        """Create Api object and login
        
        Keyword Arguments:
            server {str} -- [URL to ibp bioinformatics server] (default: {"http://bioinformatics.ibp.cz:8888/api"})
        """
       
        # retrieving data from user FIXED host login
        email = input(prompt="Enter your email\t") or "host"
        password = getpass(prompt="Enter your password\t") or "host"

        self.user = User(email=email, password=password, server=server)
        self.sequence = Sequence(user=self.user)
        self.g4hunter = G4Hunter(user=self.user)
        self.g4killer = G4Killer(user=self.user)
        self.p53 = P53(user=self.user)

    def __repr__(self):
        return f"<Api: {self.user.server} user: {self.user.email}>"

    def __str__(self):
        return f"Api: {self.user.server} user: {self.user.email}"
