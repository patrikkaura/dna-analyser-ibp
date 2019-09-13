# tool_interface.py
# !/usr/bin/env python3

import pandas as pd

from abc import ABCMeta, abstractmethod


class ToolInterface(metaclass=ABCMeta):
    """Interface for api endpoint caller has to have at least this methods"""

    @abstractmethod
    def run_tool(self, *args) -> pd.DataFrame:
        raise NotImplementedError("You should implement this!")
