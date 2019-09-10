# analyse_caller.py
# !/usr/bin/env python3
"""Library with Analyse object.
Available classes:
Analyse - class for derived  classes g4hunter, palindrome, p53 ...
AnalyseFactory - abstract class for FACTORY METHOD pattern
"""

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
        """Returns pandas dataframe for current object
        
        Returns:
            pd.DataFrame -- [pandas dataframe of analyse object]
        """
        data_frame = pd.DataFrame().from_records(
            self.__dict__, columns=self.__dict__.keys(), index=[0]
        )
        return data_frame


class AnalyseFactory(metaclass=abc.ABCMeta):
    """Abstract class for others analyse factories"""

    def __init__(self, **kwargs):
        self.analyse = self.create_analyse(**kwargs)

    @abc.abstractmethod
    def create_analyse(self, **kwargs):
        """Creates analyse with different calls on Api"""
        raise NotImplementedError("You should implement this!")
