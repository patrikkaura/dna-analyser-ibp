# g4killer_interface.py

from typing import TYPE_CHECKING

import pandas as pd

from DNA_analyser_IBP.interfaces.tool_interface import ToolInterface
from DNA_analyser_IBP.ports import Ports
from DNA_analyser_IBP.utils import exception_handler

if TYPE_CHECKING:
    from DNA_analyser_IBP.models import G4Killer as AnalyseModel


class G4Killer(ToolInterface):
    """Api interface for g4killer analyse caller"""

    def __init__(self, ports: Ports):
        self.__ports = ports

    @exception_handler
    def run(
        self, complementary: bool = False, *, sequence: str, threshold: float
    ) -> pd.DataFrame:
        """
        Run G4killer tool

        Args:
            complementary (bool): True if use for C sequence False for G sequence [default=False]
            sequence (str): original sequence
            threshold (float): G4hunter target score in interval (0;4)

        Returns:
            pd.DataFrame: DataFrame with G4killer result
        """
        result: "AnalyseModel" = self.__ports.g4killer.create_analyse(
            sequence=sequence, threshold=threshold, complementary=complementary,
        )

        return result.get_data_frame().T
