# p53_interface.py

from typing import TYPE_CHECKING

import pandas as pd

from DNA_analyser_IBP.interfaces.tool_interface import ToolInterface
from DNA_analyser_IBP.ports import Ports
from DNA_analyser_IBP.utils import exception_handler

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
