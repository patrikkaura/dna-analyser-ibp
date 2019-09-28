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
    seq_delete,
    seq_load_all,
    seq_load_by_id,
    seq_load_data,
)


class Sequence:
    def __init__(self, user: User):
        self.__user = user

    def load_all(self, filter_tag: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Return all or filtered sequences in dataframe
        :param filter_tag: tags for sequence filtering [default=None]
        :return: dataframe with sequences
        """
        seq = [se for se in seq_load_all(user=self.__user, filter_tag=filter_tag if filter_tag is not None else list())]
        data = pd.concat([s.get_dataframe() for s in seq], ignore_index=True)
        return data

    def load_by_id(self, *, id: str) -> pd.DataFrame:
        """
        Return sequence in dataframe
        :param id: sequence id
        :return: dataframe with sequence
        """
        seq = seq_load_by_id(user=self.__user, id=id)
        return seq.get_dataframe()

    def load_data(self, data_length: Optional[int] = 100, possition: Optional[int] = 0, *, sequence: pd.Series) -> str:
        """
        Return slice of sequence data in string
        :param sequence: sequence series
        :param data_length: sequence length [default=100]
        :param possition: start position [default=0]
        :return: part of sequence data
        """
        if isinstance(sequence, pd.Series):
            return seq_load_data(user=self.__user,
                                 id=sequence["id"],
                                 data_len=data_length,
                                 pos=possition,
                                 seq_len=sequence["length"])
        else:
            raise ("You have to insert pd.Series")

    def text_creator(self, circular: bool = True, tags: Optional[List[str]] = None, sequence_type: str = 'DNA', *, data: str, name: str) -> None:
        """
        Create sequence from string
        :param circular: True if sequence is circular False if not [default=True]
        :param data: sequence string
        :param name: sequence name
        :param tags: tags for sequence filtering [default=None]
        :param sequence_type: string DNA / RNA [default=DNA]
        :return:
        """
        # start Text sequence factory
        status_bar(user=self.__user,
                   func=lambda: TextSequenceFactory(
                       user=self.__user,
                       circular=circular,
                       data=data,
                       name=name,
                       tags=tags if tags is not None else list(),
                       sequence_type=sequence_type,
                   ),
                   name=name,
                   cls_switch=True)

    def ncbi_creator(self, tags: Optional[List[str]] = None, circular: bool = True, *, name: str, ncbi_id: str) -> None:
        """
        Create sequence from NCBI
        :param circular: True if sequence is circular False if not [default=True]
        :param name: sequence name
        :param tags: tags for sequence filtering [default=None]
        :param ncbi_id: sequence id from https://www.ncbi.nlm.nih.gov/
        :return:
        """
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

    def file_creator(self, tags: Optional[List[str]] = None, circular: bool = True, sequence_type: str = 'DNA', *, file_path: str, name: str, format: str) -> None:
        """
        Create sequence from TEXT / FASTA file
        :param circular: True if sequence is circular False if not [default=True]
        :param file_path: absolute path to file
        :param name: sequence name
        :param tags: tags for sequence filtering
        :param sequence_type: string DNA / RNA [default=DNA]
        :param format: string FASTA / PLAIN
        :return:
        """
        # start File sequence factory
        status_bar(user=self.__user,
                   func=lambda: FileSequenceFactory(
                       user=self.__user,
                       circular=circular,
                       file_path=file_path,
                       name=name,
                       tags=tags if tags is not None else list(),
                       sequence_type=sequence_type,
                       format=format,
                   ),
                   name=name,
                   cls_switch=True)

    def delete(self, *, sequence_dataframe: Union[pd.DataFrame, pd.Series]) -> None:
        """
        Delete sequence
        :param sequence_dataframe:
            sequence_dataframe {Union[pd.DataFrame, pd.Series]} -- [
        :return:
        """
        if isinstance(sequence_dataframe, pd.DataFrame):
            for _, row in sequence_dataframe.iterrows():
                _id = row["id"]
                if seq_delete(user=self.__user, id=_id):
                    print(f"Sequence {_id} was deleted")
                    time.sleep(1)
                else:
                    print("Sequence cannot be deleted")
        else:
            _id = sequence_dataframe["id"]
            if seq_delete(user=self.__user, id=_id):
                print(f"Sequence {_id} was deleted")
            else:
                print("Sequence cannot be deleted")
