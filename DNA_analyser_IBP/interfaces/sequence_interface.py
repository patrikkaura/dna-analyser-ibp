# sequence_interface.py

import time
from typing import List, Optional, Union

import pandas as pd

from DNA_analyser_IBP.models import Sequence as Data
from DNA_analyser_IBP.ports import Ports
from DNA_analyser_IBP.statusbar import status_bar
from DNA_analyser_IBP.type import Types
from DNA_analyser_IBP.utils import (
    Logger,
    _multifasta_parser,
    exception_handler,
    normalize_name,
)


class Sequence:
    def __init__(self, ports: Ports):
        self.__ports = ports

    @exception_handler
    def load_all(self, tags: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Return all or filtered sequences in DataFrame

        Args:
            tags (Optional[List[str]]): tags for sequence filtering [default=None]

        Returns:
            pd.DataFrame: DataFrame with sequences
        """
        listed_sequences: list = [
            sequence
            for sequence in self.__ports.sequence.load_all(
                tags=tags if tags is not None else list()
            )
        ]

        data: pd.DataFrame = pd.concat(
            [sequence.get_data_frame() for sequence in listed_sequences],
            ignore_index=True,
        )

        return data

    @exception_handler
    def load_by_id(self, *, id: str) -> pd.DataFrame:
        """
        Return sequence in DataFrame

        Args:
            id (str): sequence id

        Returns:
            pd.DataFrame: DataFrame with sequence
        """

        sequence: "Data" = self.__ports.sequence.load_by_id(id=id)

        return sequence.get_data_frame()

    @exception_handler
    def load_data(
        self,
        length: Optional[int] = 100,
        position: Optional[int] = 0,
        *,
        sequence: Union[pd.Series, pd.DataFrame],
    ) -> str:
        """
        Return slice of sequence data in string

        Args:
            length (Optional[int]): sequence data length in interval <0;1000> [default=100]
            position (Optional[int]): data start position [default=0]
            sequence (Union[pd.Series, pd.DataFrame]): sequence in pd.Series

        Returns:
            str: sequence data
        """

        def _load_data(*, id: str, sequence_length: int):
            return self.__ports.sequence.load_data(
                id=id,
                length=length,
                position=position,
                sequence_length=sequence_length,
            )

        if isinstance(sequence, pd.DataFrame):
            return _load_data(
                id=sequence.iloc[0]["id"], sequence_length=sequence.iloc[0]["length"]
            )
        elif isinstance(sequence, pd.Series):
            return _load_data(id=sequence["id"], sequence_length=sequence["length"])
        else:
            Logger.error("Parameter sequence have to be pd.DataFrame or pd.Series!")

    @exception_handler
    def text_creator(
        self,
        circular: bool = True,
        tags: Optional[List[str]] = None,
        nucleic_type: str = "DNA",
        *,
        string: str,
        name: str,
    ) -> None:
        """
        Create sequence from string

        Args:
            circular (bool): True if sequence is circular False if not [default=True]
            tags (Optional[List[str]]): tags for sequence filtering [default=None]
            nucleic_type (str): string DNA|RNA [default=DNA]
            string (str): sequence string
            name (str): sequence name
        """
        name: str = normalize_name(name=name)

        status_bar(
            ports=self.__ports,
            func=lambda: self.__ports.sequence.create_text_sequence(
                circular=circular,
                data=string,
                name=name,
                tags=tags if tags is not None else list(),
                nucleic_type=nucleic_type,
            ),
            name=name,
            type=Types.SEQUENCE,
        )

    @exception_handler
    def ncbi_creator(
        self,
        tags: Optional[List[str]] = None,
        circular: bool = True,
        *,
        name: str,
        ncbi_id: str,
    ) -> None:
        """
        Create sequence from NCBI

        Args:
            tags (Optional[List[str]]): tags for sequence filtering [default=None]
            circular (bool): True if sequence is circular False if not [default=True]
            name (str): sequence name
            ncbi_id (str): sequence id from https://www.ncbi.nlm.nih.gov/
        """
        name: str = normalize_name(name=name)

        status_bar(
            ports=self.__ports,
            func=lambda: self.__ports.sequence.create_ncbi_sequence(
                circular=circular,
                name=name,
                tags=tags if tags is not None else list(),
                ncbi_id=ncbi_id,
            ),
            name=name,
            type=Types.SEQUENCE,
        )

    @exception_handler
    def file_creator(
        self,
        tags: Optional[List[str]] = None,
        circular: bool = True,
        nucleic_type: str = "DNA",
        *,
        path: str,
        name: str,
        format: str,
    ) -> None:
        """
        Create sequence from [TEXT|FASTA] file

        Args:
            tags (Optional[List[str]]): tags for sequence filtering [default=None]
            circular (bool): True if sequence is circular False if not [default=True]
            name (str): sequence name
            nucleic_type (str): string DNA|RNA [default=DNA]
            format (str): string FASTA|PLAIN
            path (str): absolute path to [TEXT|FASTA] file
        """
        name: str = normalize_name(name=name)

        status_bar(
            ports=self.__ports,
            func=lambda: self.__ports.sequence.create_file_sequence(
                circular=circular,
                path=path,
                name=name,
                tags=tags if tags is not None else list(),
                nucleic_type=nucleic_type,
                format=format,
            ),
            name=name,
            type=Types.SEQUENCE,
        )

    @exception_handler
    def multifasta_creator(
        self,
        tags: Optional[List[str]] = None,
        circular: bool = False,
        *,
        path: str,
        nucleic_type: str,
    ) -> None:
        """
        Create sequence from [MultiFASTA] file

        Args:
            tags (Optional[List[str]]): tags for sequence filtering [default=None]
            circular (bool): True if sequence is circular False if not [default=True]
            nucleic_type (str): string DNA|RNA [default=DNA]
            path (str): absolute path to [TEXT|FASTA] file
        """
        for sequence_name, sequence_nucleic in _multifasta_parser(path=path):
            sequence_name: str = normalize_name(name=sequence_name)

            status_bar(
                ports=self.__ports,
                func=lambda: self.__ports.sequence.create_text_sequence(
                    circular=circular,
                    data=sequence_nucleic,
                    name=sequence_name,
                    tags=tags if tags is not None else list(),
                    nucleic_type=nucleic_type,
                ),
                name=sequence_name,
                type=Types.SEQUENCE,
            )

    @exception_handler
    def delete(self, *, sequence: Union[pd.DataFrame, pd.Series]) -> None:
        """
        Delete sequence by given pandas DataFrame or Series

        Args:
            sequence (Union[pd.DataFrame, pd.Series]): sequence or multiple sequences
        """

        def _delete(id: str) -> None:
            if self.__ports.sequence.delete(id=id):
                Logger.info(f"Sequence {id} was deleted!")
                time.sleep(1)
            else:
                Logger.error(f"Sequence {id} cannot be deleted!")

        if isinstance(sequence, pd.DataFrame):
            for _, row in sequence.iterrows():
                _delete(row["id"])
        else:
            _delete(sequence["id"])

    @exception_handler
    def nucleic_count(self, *, sequence: Union[pd.DataFrame, pd.Series]) -> None:
        """
        Re-count nucleotides for given sequence pandas DataFrame or Series

        Args:
            sequence (Union[pd.DataFrame, pd.Series]): sequence or multiple sequences
        """

        def _nucleic_count(id: str) -> None:
            if self.__ports.sequence.nucleic_count(id=id):
                Logger.info(f"Sequence {id} nucleotides was re-counted!")
            else:
                Logger.error(f"Sequence {id} nucleotides cannot be re-counted!")

        if isinstance(sequence, pd.DataFrame):
            for _, row in sequence.iterrows():
                _nucleic_count(row["id"])
        else:
            _nucleic_count(sequence["id"])
