# sequence_interface.py
# !/usr/bin/env python3
"""Library with Sequence interface object
Available classes:
Sequence - interface for interaction with sequence api
"""

import time
import pandas as pd

from typing import List, Union
from ..callers.user_caller import User

from ..statusbar import status_bar

from ..callers.sequence_caller import (
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

    def load_all(self, filter_tag: List[str] = None) -> pd.DataFrame:
        """Return all or filtered sequences in dataframe
        
        Keyword Arguments:
            filter_tag {List[str]} -- [tags for sequence filtering] (default: {None})
        
        Returns:
            pd.DataFrame -- [dataframe with sequences]
        """

        seq = [se for se in seq_load_all(user=self.__user, filter_tag=filter_tag)]
        data = pd.concat([s.get_dataframe() for s in seq], ignore_index=True)
        
        return data

    def load_by_id(self, id: str) -> pd.DataFrame:
        """Return sequence in dataframe
        
        Arguments:
            id {str} -- [sequence id]
        
        Returns:
            pd.DataFrame -- [dataframe with sequence]
        """

        seq = seq_load_by_id(user=self.__user, id=id)
        
        return seq.get_dataframe()

    def load_data(self, sequence: pd.Series, data_len: int = 100, pos: int = 0) -> str:
        """Return slice of sequence data in string
        
        Arguments:
            sequence {pd.Series} -- [sequence series]
        
        Keyword Arguments:
            data_len {int} -- [sequence length] (default: {100})
            pos {int} -- [start position] (default: {0})
        
        Returns:
            str -- [description]
        """

        if isinstance(sequence, pd.Series):
            return seq_load_data(
                user=self.__user,
                id=sequence["id"],
                data_len=data_len,
                pos=pos,
                seq_len=sequence["length"],
            )
        else:
            raise ("You have to insert pd.Series")

    def text_creator(
        self, circular: bool, data: str, name: str, tags: List[str], sequence_type: str
    ):
        """Create sequence from string
        
        Arguments:
            circular {bool} -- [True if sequence is circular False if not]
            data {str} -- [sequence string]
            name {str} -- [sequence name]
            tags {List[str]} -- [tags for sequence filtering]
            sequence_type {str} -- [string DNA / RNA]
        """
        # start Text sequence factory
        status_bar(
            user=self.__user,
            func=lambda: TextSequenceFactory(
                user=self.__user,
                circular=circular,
                data=data,
                name=name,
                tags=tags,
                sequence_type=sequence_type,
            ),
            name=name,
            cls_switch=True,
        )

    def ncbi_creator(self, circular: bool, name: str, tags: List[str], ncbi_id: str):
        """Create sequence from NCBI
        
        Arguments:
            circular {bool} -- [True if sequence is circular False if not]
            name {str} -- [sequence name]
            tags {List[str]} -- [tags for sequence filtering]
            ncbi_id {str} -- [sequence id from (https://www.ncbi.nlm.nih.gov/)]
        """

        # start NCBI sequence factory
        status_bar(
            user=self.__user,
            func=lambda: NCBISequenceFactory(
                user=self.__user,
                circular=circular,
                name=name,
                tags=tags,
                ncbi_id=ncbi_id,
            ),
            name=name,
            cls_switch=True,
        )

    def file_creator(
        self,
        circular: bool,
        file_path: str,
        name: str,
        tags: List[str],
        sequence_type: str,
        format: str,
    ):
        """Create sequence from TEXT / FASTA file
        
        Arguments:
            circular {bool} -- [True if sequence is circular False if not]
            file_path {str} -- [absolute path to file]
            name {str} -- [sequence name]
            tags {List[str]} -- [tags for sequence filtering]
            sequence_type {str} -- [string DNA / RNA]
            format {str} -- [string FASTA / PLAIN]
        """

        # start File sequence factory
        status_bar(
            user=self.__user,
            func=lambda: FileSequenceFactory(
                user=self.__user,
                circular=circular,
                file_path=file_path,
                name=name,
                tags=tags,
                sequence_type=sequence_type,
                format=format,
            ),
            name=name,
            cls_switch=True,
        )

    def delete(self, sequence_dataframe: Union[pd.DataFrame, pd.Series]):
        """Delete sequence
        
        Arguments:
            sequence_dataframe {Union[pd.DataFrame, pd.Series]} -- [sequence dataframe / series]
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
