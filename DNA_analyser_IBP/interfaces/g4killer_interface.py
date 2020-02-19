# g4killer_interface.py
# !/usr/bin/env python3

import pandas as pd

from .tool_interface import ToolInterface
from ..callers import G4KillerAnalyseFactory, User
from ..utils import exception_handler


class G4Killer(ToolInterface):
    """Api interface for g4killer analyse caller"""

    def __init__(self, user: User):
        self.__user = user

    @exception_handler
    def run(self, complementary: bool = False, *, sequence: str, threshold: float) -> pd.DataFrame:
        """
        Run G4killer tool

        Args:
            complementary (bool): True if use for C sequence False for G sequence [default=False]
            sequence (str): original sequence
            threshold (float): G4hunter target score in interval (0;4)

        Returns:
            pd.DataFrame: Dataframe with G4killer result
        """
        result = G4KillerAnalyseFactory(user=self.__user, sequence=sequence, threshold=threshold, complementary=complementary).analyse
        return result.get_dataframe().T
