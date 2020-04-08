# api.py
# !/usr/bin/env python3
"""
Module with API object for manipulation with BPI REST API.
"""
from getpass import getpass

from DNA_analyser_IBP.callers import User
from DNA_analyser_IBP.utils import Logger
from DNA_analyser_IBP.singleton import Singleton
from DNA_analyser_IBP.interfaces import G4Hunter, Sequence, G4Killer, P53, Extras


class Api(metaclass=Singleton):
    """Api class contains all methods for working with BPI REST API."""

    def __init__(self, *, server: str = "http://bioinformatics.ibp.cz:8888/api"):
        """
        Create API object and login

        Args:
            server (str): URL to ibp bioinformatics server [Default=http://bioinformatics.ibp.cz:8888/api]
        """
        # retrieve data from user, default = host accont
        email: str = input("Enter your email\t") or "host"
        password: str = getpass("Enter your password\t", stream=None) or "host"
        Logger.info(f"User {email} is trying to login ...")

        self.user: User = User(email=email, password=password, server=server)
        self.sequence: Sequence = Sequence(user=self.user)
        self.g4hunter: G4Hunter = G4Hunter(user=self.user)
        self.g4killer: G4Killer = G4Killer(user=self.user)
        self.p53_predictor: P53 = P53(user=self.user)
        self.tools: Extras = Extras()

    def __repr__(self):
        return f"<Api: {self.user.server} user: {self.user.email}>"

    def __str__(self):
        return f"Api: {self.user.server} user: {self.user.email}"
