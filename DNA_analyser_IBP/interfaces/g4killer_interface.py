# g4killer_interface.py
# !/usr/bin/env python3

import pandas as pd

from .tool_interface import ToolInterface
from ..callers import G4KillerAnalyseFactory, User


class G4Killer(ToolInterface):
    """Api interface for g4killer analyse caller"""

    def __init__(self, user: User):
        self.__user = user

    def run_tool(self, on_complementary: bool = False, *, origin_sequence: str, threshold: float) -> pd.DataFrame:
        """
        Run G4killer tool
        :param origin_sequence: original sequence
        :param threshold: g4hunter target gscore
        :param on_complementary: True if use for C sequence False for G sequence [default=False]
        :return: dataframe with g4killer result
        """
        gkill = G4KillerAnalyseFactory(user=self.__user, origin_sequence=origin_sequence, threshold=threshold, on_complementary=on_complementary).analyse
        return gkill.get_dataframe().T
