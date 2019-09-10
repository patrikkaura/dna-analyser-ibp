# p53_interface.py
# !/usr/bin/env python3
"""Library with P53 interface object
Available classes:
P53 - interface for interaction with p53 api
"""

import pandas as pd

from .tool_interface import ToolInterface
from ..callers.user_caller import User
from ..callers.p53_caller import P53AnalyseFactory


class P53(ToolInterface):
    """Api interface for p53 caller"""

    def __init__(self, user: User):
        self.__user = user

    def run_tool(self, sequence: str) -> pd.DataFrame:
        """Run P53 tool
        
        Arguments:
            sequence {str} -- [sequence to analyse length = 20]
        
        Returns:
            pd.DataFrame -- [dataframe with p53 result]
        """
        
        p53kill = P53AnalyseFactory(user=self.__user, sequence=sequence.strip()).analyse
        
        return p53kill.get_dataframe().T
