# base_connector.py

import abc

from DNA_analyser_IBP.models.user import User


class BaseAdapter:
    def __init__(self, user: User) -> None:
        self.user = user


class BaseAnalyseAdapter(metaclass=abc.ABCMeta):
    """
    Abstract class for others connectors factories
    """

    def __init__(self, **kwargs):
        self.analyse = self.create_analyse(**kwargs)

    @abc.abstractmethod
    def create_analyse(self, **kwargs):
        """Creates analyse with different calls on Api"""
        raise NotImplementedError("You should implement this!")
