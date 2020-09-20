# p53_interface.py

from typing import TYPE_CHECKING, List

import pandas as pd

from DNA_analyser_IBP.interfaces.tool_interface import ToolInterface
from DNA_analyser_IBP.ports import Ports
from DNA_analyser_IBP.utils import exception_handler
from DNA_analyser_IBP.utils import Logger

if TYPE_CHECKING:
    from DNA_analyser_IBP.models import P53 as AnalyseModel


class P53(ToolInterface):
    """Api interface for p53 caller"""

    def __init__(self, ports: Ports):
        self.__ports = ports

    @exception_handler
    def run(self, *, sequence: str) -> pd.DataFrame:
        """
        Run P53 tool

        Args:
            sequence (str): sequence [length=20] to analyse

        Returns:
            pd.DataFrame: DataFrame with P53predictor result
        """
        p53killer: "AnalyseModel" = self.__ports.p53.create_analyse(
            sequence=sequence.strip()
        )
        return p53killer.get_data_frame().T

    @exception_handler
    def run_multiple(self, *, sequences: List[str]) -> pd.DataFrame:
        """
        Run P53 tool for multiple sequences

        Args:
            sequences (List[str]): list of sequences sequence [length=20] to analyse

        Returns:
            pd.DataFrame: DataFrame with P53predictor result
        """
        if sequences:
            list_p53: list = [
                self.__ports.p53.create_analyse(sequence=sequence)
                for sequence in sequences
            ]
            data: pd.DataFrame = pd.concat(
                [p53.get_data_frame() for p53 in list_p53],
                ignore_index=True,
            )
            return data
        else:
            Logger.error("You should provide sequence list!")
