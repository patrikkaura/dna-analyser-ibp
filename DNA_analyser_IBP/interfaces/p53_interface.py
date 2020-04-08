# p53_interface.py
# !/usr/bin/env python3

import pandas as pd

from DNA_analyser_IBP.utils import exception_handler
from DNA_analyser_IBP.interfaces.tool_interface import ToolInterface
from DNA_analyser_IBP.callers import User, P53AnalyseFactory, P53Analyse


class P53(ToolInterface):
    """Api interface for p53 caller"""

    def __init__(self, user: User):
        self.__user = user

    @exception_handler
    def run(self, *, sequence: str) -> pd.DataFrame:
        """
        Run P53 tool

        Args:
            sequence (str): sequence [length=20] to analyse

        Returns:
            pd.DataFrame: Dataframe with P53predictor result
        """
        p53kill: P53Analyse = P53AnalyseFactory(
            user=self.__user, sequence=sequence.strip()
        ).analyse
        return p53kill.get_dataframe().T
