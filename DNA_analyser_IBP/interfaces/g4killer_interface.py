# g4killer_interface.py

from typing import TYPE_CHECKING, List

import pandas as pd

from DNA_analyser_IBP.interfaces.tool_interface import ToolInterface
from DNA_analyser_IBP.ports import Ports
from DNA_analyser_IBP.utils import exception_handler
from DNA_analyser_IBP.utils import Logger

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
        Run G4Killer tool

        Args:
            complementary (bool): True if use for C sequence False for G sequence [default=False]
            sequence (str): original sequence
            threshold (float): G4hunter target score in interval (0;4)

        Returns:
            pd.DataFrame: DataFrame with G4Killer result
        """
        result: "AnalyseModel" = self.__ports.g4killer.create_analyse(
            sequence=sequence,
            threshold=threshold,
            complementary=complementary,
        )
        return result.get_data_frame().T

    @exception_handler
    def run_multiple(
        self, complementary: bool = False, *, sequences: List[str], threshold: float
    ) -> pd.DataFrame:
        """
        Run G4Killer tool for multiple sequences

        Args:
            complementary (bool): True if use for C sequence False for G sequence [default=False]
            sequences (List[str]): original sequences stored in list
            threshold (float): G4hunter target score in interval (0;4)

        Returns:
            pd.DataFrame: DataFrame with all G4Killer results
        """
        if sequences:
            list_g4killer: list = [
                self.__ports.g4killer.create_analyse(
                    sequence=sequence, threshold=threshold, complementary=complementary
                )
                for sequence in sequences
            ]
            data: pd.DataFrame = pd.concat(
                [g4killer.get_data_frame() for g4killer in list_g4killer],
                ignore_index=True,
            )
            return data
        else:
            Logger.error("You should provide sequence list!")
