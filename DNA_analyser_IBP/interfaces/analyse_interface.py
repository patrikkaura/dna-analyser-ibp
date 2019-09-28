# api_interface.py
# !/usr/bin/env python3

import pandas as pd
from typing import List, Union, Optional
from abc import ABCMeta, abstractmethod


class AnalyseInterface(metaclass=ABCMeta):
    """Interface for api endpoint caller has to have at least this methods"""

    @abstractmethod
    def load_all(self, filter_tag: Optional[List[str]]) -> pd.DataFrame:
        raise NotImplementedError("You should implement this!")

    @abstractmethod
    def load_by_id(self, id: str) -> pd.DataFrame:
        raise NotImplementedError("You should implement this!")

    @abstractmethod
    def delete(self, obj: Union[pd.DataFrame, pd.Series]):
        raise NotImplementedError("You should implement this!")

    @abstractmethod
    def analyse_creator(self, *args):
        raise NotImplemented("You should implement this!")
