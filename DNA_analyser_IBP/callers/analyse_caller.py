# analyse_caller.py
# !/usr/bin/env python3

import abc
import pandas as pd


class AnalyseModel:
    """Analyse class used in g4hunter + palindrome analyse"""

    def __init__(self, **kwargs):
        self.id = kwargs.pop("id")
        self.created = kwargs.pop("created")
        self.tags = ", ".join(kwargs.pop("tags"))
        self.finished = kwargs.pop("finished")
        self.title = kwargs.pop("title")
        self.sequence_id = kwargs.pop("sequenceId")

    def get_dataframe(self) -> pd.DataFrame:
        """
        Return pandas dataframe for current object
        :return: dataframe with object data
        """
        data_frame = pd.DataFrame().from_records(self.__dict__, columns=self.__dict__.keys(), index=[0])
        return data_frame


class AnalyseFactory(metaclass=abc.ABCMeta):
    """Abstract class for others analyse factories"""

    def __init__(self, **kwargs):
        self.analyse = self.create_analyse(**kwargs)

    @abc.abstractmethod
    def create_analyse(self, **kwargs):
        """Creates analyse with different calls on Api"""
        raise NotImplementedError("You should implement this!")
