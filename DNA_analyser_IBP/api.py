# api.py
# !/usr/bin/env python3
"""
Module with API object for manipulation with BPI REST API.
"""

from getpass import getpass

from DNA_analyser_IBP.utils import Logger
from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.models import User
from DNA_analyser_IBP.singleton import Singleton
from DNA_analyser_IBP.adapters import UserAdapter
from DNA_analyser_IBP.interfaces import Interfaces
from DNA_analyser_IBP.ports import Ports


class Api(metaclass=Singleton):
    """
    Api class contains all methods for working with BPI REST API.
    """

    def __init__(self, *, server: str = Config.SERVER_CONFIG.LOCALHOST):
        """
        Create API object and login

        Args:
            server (str): URL to ibp bioinformatics server [Default=http://bioinformatics.ibp.cz:8888/api]
        """
        # retrieve data from user, default = host account
        email: str = input("Enter your email\t") or "host"
        password: str = getpass("Enter your password\t", stream=None) or "host"
        Logger.info(f"User {email} is trying to login ...")

        # user
        self.__user = UserAdapter.sign_in(User(email, password, server))
        self.__ports = Ports(user=self.__user)
        self.__interfaces = Interfaces(ports=self.__ports)

        self.sequence = self.__interfaces.sequence
        self.g4hunter = self.__interfaces.g4hunter
        self.g4killer = self.__interfaces.g4killer
        self.p53_predictor = self.__interfaces.p53_predictor
        self.rloopr = self.__interfaces.rloopr
        self.tools = self.__interfaces.extras


def __repr__(self):
    return f"<Api: {self.user.server} user: {self.user.email}>"


def __str__(self):
    return f"Api: {self.user.server} user: {self.user.email}"
