# g4killer_interface.py
# !/usr/bin/env python3
"""Library with G4killer interface object
Available classes:
G4Killer - interface for interaction with g4killer api
"""
import pandas as pd

from ..callers.g4killer_caller import G4KillerAnalyseFactory
from ..callers.user_caller import User
from .tool_interface import ToolInterface


class G4Killer(ToolInterface):
    """Api interface for g4killer analyse caller"""

    def __init__(self, user: User):
        self.__user = user

    def run_tool(self, origin_sequence: str, threshold: float) -> pd.DataFrame:
        """Run G4killer tool
        
        Arguments:
            origin_sequence {str} -- [original sequence]
            threshold {float} -- [g4hunter target gscore]
        
        Returns:
            pd.DataFrame -- [dataframe with g4killer result]
        """
       
        gkill = G4KillerAnalyseFactory(
            user=self.__user, origin_sequence=origin_sequence, threshold=threshold
        ).analyse

        return gkill.get_dataframe().T
