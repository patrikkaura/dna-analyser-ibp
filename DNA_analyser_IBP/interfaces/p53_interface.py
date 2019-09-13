# p53_interface.py
# !/usr/bin/env python3

import pandas as pd

from .tool_interface import ToolInterface
from ..callers import User, P53AnalyseFactory


class P53(ToolInterface):
    """Api interface for p53 caller"""

    def __init__(self, user: User):
        self.__user = user

    def run_tool(self, *, sequence: str) -> pd.DataFrame:
        """
        Run P53 tool
        :param sequence: sequence to analyse of length 20
        :return: dataframe with p53 result
        """
        p53kill = P53AnalyseFactory(user=self.__user, sequence=sequence.strip()).analyse
        return p53kill.get_dataframe().T
