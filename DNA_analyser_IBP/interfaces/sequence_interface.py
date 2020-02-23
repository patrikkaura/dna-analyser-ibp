# sequence_interface.py
# !/usr/bin/env python3

import time
import pandas as pd
from typing import List, Union, Optional

from ..statusbar import status_bar
from ..callers import (
    User,
    NCBISequenceFactory,
    TextSequenceFactory,
    FileSequenceFactory,
    SequenceMethods
)
from ..utils import exception_handler, Logger, normalize_name, _multifasta_parser


class Sequence:
    def __init__(self, user: User):
        self.__user = user

    @exception_handler
    def load_all(self, tags: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Return all or filtered sequences in dataframe

        Args:
            tags (Optional[List[str]]): tags for sequence filtering [default=None]

        Returns:
            pd.DataFrame: Dataframe with sequences
        """
        seq = [se for se in SequenceMethods.load_all(user=self.__user, tags=tags if tags is not None else list())]
        data = pd.concat([s.get_dataframe() for s in seq], ignore_index=True)
        return data

    @exception_handler
    def load_by_id(self, *, id: str) -> pd.DataFrame:
        """
        Return sequence in dataframe

        Args:
            id (str): sequence id

        Returns:
            pd.DataFrame: Dataframe with sequence
        """
        seq = SequenceMethods.load_by_id(user=self.__user, id=id)
        return seq.get_dataframe()

    @exception_handler
    def load_data(self, length: Optional[int] = 100, possition: Optional[int] = 0, *, sequence: pd.Series) -> str:
        """
        Return slice of sequence data in string

        Args:
            length (Optional[int]): sequence data length in interval <0;1000> [default=100]
            possition (Optional[int]): data start position [default=0]
            sequence (pd.Series): sequence in pd.Series

        Returns:
            str: sequence data
        """
        if isinstance(sequence, pd.Series):
            return SequenceMethods.load_data(user=self.__user,
                                             id=sequence["id"],
                                             length=length,
                                             possiotion=possition,
                                             sequence_length=sequence["length"])
        else:
            Logger.error("Parameter sequence have to be pd.Series!")

    @exception_handler
    def text_creator(self, circular: bool = True, tags: Optional[List[str]] = None, nucleic_type: str = 'DNA', *, string: str, name: str) -> None:
        """
        Create sequence from string

        Args:
            circular (bool): True if sequence is circular False if not [default=True]
            tags (Optional[List[str]]): tags for sequence filtering [default=None]
            nucleic_type (str): string DNA|RNA [default=DNA]
            string (str): sequence string
            name (str): sequence name
        """
        name = normalize_name(name=name)
        # start Text sequence factory
        status_bar(user=self.__user,
                   func=lambda: TextSequenceFactory(
                       user=self.__user,
                       circular=circular,
                       data=string,
                       name=name,
                       tags=tags if tags is not None else list(),
                       nucleic_type=nucleic_type,
                   ),
                   name=name,
                   cls_switch=True)

    @exception_handler
    def ncbi_creator(self, tags: Optional[List[str]] = None, circular: bool = True, *, name: str, ncbi_id: str) -> None:
        """
        Create sequence from NCBI

        Args:
            tags (Optional[List[str]]): tags for sequence filtering [default=None]
            circular (bool): True if sequence is circular False if not [default=True]
            name (str): sequence name
            ncbi_id (str): sequence id from https://www.ncbi.nlm.nih.gov/
        """
        name = normalize_name(name=name)
        # start NCBI sequence factory
        status_bar(user=self.__user,
                   func=lambda: NCBISequenceFactory(
                       user=self.__user,
                       circular=circular,
                       name=name,
                       tags=tags if tags is not None else list(),
                       ncbi_id=ncbi_id,
                   ),
                   name=name,
                   cls_switch=True)

    @exception_handler
    def file_creator(self, tags: Optional[List[str]] = None, circular: bool = True, nucleic_type: str = 'DNA', *, path: str, name: str, format: str) -> None:
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
        name = normalize_name(name=name)
        # start File sequence factory
        status_bar(user=self.__user,
                   func=lambda: FileSequenceFactory(
                       user=self.__user,
                       circular=circular,
                       path=path,
                       name=name,
                       tags=tags if tags is not None else list(),
                       nucleic_type=nucleic_type,
                       format=format,
                   ),
                   name=name,
                   cls_switch=True)

    @exception_handler
    def multifasta_creator(self, tags: Optional[List[str]] = None, circular: bool = False, *, path: str, nucleic_type: str) -> None:
        """
        Create sequence from [MultiFASTA] file

        Args:
            tags (Optional[List[str]]): tags for sequence filtering [default=None]
            circular (bool): True if sequence is circular False if not [default=True]
            nucleic_type (str): string DNA|RNA [default=DNA]
            path (str): absolute path to [TEXT|FASTA] file
        """
        for sequence_name, sequence_nucleic in _multifasta_parser(path=path):
            sequence_name = normalize_name(name=sequence_name)
            status_bar(user=self.__user,
                       func=lambda: TextSequenceFactory(
                           user=self.__user,
                           circular=circular,
                           data=sequence_nucleic,
                           name=sequence_name,
                           tags=tags if tags is not None else list(),
                           nucleic_type=nucleic_type,
                       ),
                       name=sequence_name,
                       cls_switch=True)

    @exception_handler
    def delete(self, *, sequence: Union[pd.DataFrame, pd.Series]) -> None:
        """
        Delete sequence by given dataframe|series

        Args:
            sequence (Union[pd.DataFrame, pd.Series]): sequence or multiple sequences
        """
        if isinstance(sequence, pd.DataFrame):
            for _, row in sequence.iterrows():
                _id = row["id"]
                if SequenceMethods.delete(user=self.__user, id=_id):
                    Logger.info(f"Sequence {_id} was deleted!")
                    time.sleep(1)
                else:
                    Logger.error(f"Sequence {_id} cannot be deleted!")
        else:
            _id = sequence["id"]
            if SequenceMethods.delete(user=self.__user, id=_id):
                Logger.info(f"Sequence {_id} was deleted!")
            else:
                Logger.error(f"Sequence {_id} cannot be deleted!")

    @exception_handler
    def nucleic_count(self, *, sequence: Union[pd.DataFrame, pd.Series]) -> None:
        """
        Re-count nucleotides for given sequence dataframe|series

        Args:
            sequence (Union[pd.DataFrame, pd.Series]): sequence or multiple sequences
        """
        if isinstance(sequence, pd.DataFrame):
            for _, row in sequence.iterrows():
                _id = row["id"]
                if SequenceMethods.nucleic_count(user=self.__user, id=_id):
                    Logger.info(f"Sequence {_id} nucleotides was re-counted!")
                else:
                    Logger.error(f"Sequence {_id} nucleotides cannot be re-counted!")
