# tool_interface.py
# !/usr/bin/env python3

from abc import ABCMeta, abstractmethod

import pandas as pd


class ToolInterface(metaclass=ABCMeta):
    """Interface for api endpoint caller has to have at least this methods"""

    @abstractmethod
    def run(self, *args) -> pd.DataFrame:
        raise NotImplementedError("You should implement this!")
