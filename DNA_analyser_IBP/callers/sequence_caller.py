# sequence_caller.py
# !/usr/bin/env python3

import abc
import json
import requests
import pandas as pd
from requests_toolbelt import MultipartEncoder
from typing import Generator, List, Optional

from .user_caller import User
from ..utils import validate_key_response, validate_text_response, Logger


class SequenceModel:
    """Sequence class"""

    def __init__(self, **kwargs):
        self.id = kwargs.pop("id")
        self.name = kwargs.pop("name")
        self.created = kwargs.pop("created")
        self.type = kwargs.pop("type")
        self.circular = kwargs.pop("circular")
        self.length = kwargs.pop("length")
        self.ncbi = kwargs.pop("ncbi")
        self.tags = ", ".join(kwargs.pop("tags"))
        self.fasta_comment = kwargs.pop("fastaComment")
        self.gc_count, self.nucleic_count = None, None
        self.set_gc_count(kwargs.pop("nucleicCounts"))

    def __str__(self):
        return f"Sequence {self.id} {self.name} {self.type}"

    def __repr__(self):
        return f"<Sequence {self.id} {self.name} {self.type}>"

    def set_gc_count(self, nucleic_dict: dict) -> None:
        """
        Set GC count from nucleic count dict

        Args:
            nucleic_dict (dict): structure with Guanine and Cytosine counts
        """
        if nucleic_dict is not None:
            self.gc_count = int(nucleic_dict.get('C', 0)) + int(nucleic_dict.get('G', 0))
            self.nucleic_count = str(nucleic_dict)

    def get_dataframe(self) -> pd.DataFrame:
        """
        Return pandas dataframe for current object

        Returns:
            pd.DataFrame: dataframe with object data
        """
        data = pd.DataFrame().from_records(self.__dict__, columns=self.__dict__.keys(), index=[0])
        return data


class SequenceFactory(metaclass=abc.ABCMeta):
    """Abstract class for others sequence factories"""

    def __init__(self, **kwargs):
        self.sequence = self.create_sequence(**kwargs)

    @abc.abstractmethod
    def create_sequence(self, **kwargs) -> SequenceModel:
        """Creates sequence with different calls on Api"""
        raise NotImplementedError("You should implement this!")


class TextSequenceFactory(SequenceFactory):
    """Sequence factory used for generating sequence from raw text or text file"""

    def create_sequence(self, user: User, circular: bool, data: str, name: str, tags: List[Optional[str]], nucleic_type: str) -> SequenceModel:
        """
        Text sequence factory

        Args:
            user (User): user for auth
            circular (bool): True if sequence is circular False if not
            data (str): string data with sequence
            name (str): sequence name
            tags (List[Optional[str]]): tags for sequence filtering
            nucleic_type (str): string DNA|RNA

        Returns:
            SequenceModel: Sequence object
        """
        header = {"Content-type": "application/json",
                  "Accept": "application/json",
                  "Authorization": user.jwt}
        data = json.dumps({
            "circular": circular,
            "data": data,
            "format": "PLAIN",
            "name": name,
            "tags": tags,
            "type": nucleic_type})

        response = requests.post(f"{user.server}/sequence/import/text", headers=header, data=data)
        data = validate_key_response(response=response, status_code=201, payload_key="payload")
        return SequenceModel(**data)


class FileSequenceFactory(SequenceFactory):
    """Sequence factory used for generating sequence from file"""

    def create_sequence(self, user: User, circular: bool, path: str, name: str, tags: List[Optional[str]], nucleic_type: str, format: str) -> SequenceModel:
        """
        File sequence factory

        Args:
            user (User): user for auth
            circular (bool): True if sequence is circular False if not
            path (str): absolute path to sequence file
            name (str): sequence name
            tags (List[Optional[str]]): tags for sequence filtering
            nucleic_type (str): string DNA|RNA\
            format (str): string FASTA|PLAIN

        Returns:
            SequenceModel: Sequence object
        """
        data = json.dumps({
            "circular": circular,
            "format": format,
            "name": name,
            "tags": tags,
            "type": nucleic_type})
        multi_encoder = MultipartEncoder(fields={"json": data, "file": ("filename", open(path, "rb"))})
        header = {"Content-type": multi_encoder.content_type,
                  "Accept": "application/json",
                  "Authorization": user.jwt}

        response = requests.post(f"{user.server}/sequence/import/file", headers=header, data=multi_encoder)
        data = validate_key_response(response=response, status_code=201, payload_key="payload")
        return SequenceModel(**data)


class NCBISequenceFactory(SequenceFactory):
    """Sequence factory used for generating sequence from NCBI database"""

    def create_sequence(self, user: User, circular: bool, name: str, tags: List[Optional[str]], ncbi_id: str) -> SequenceModel:
        """
        NCBI sequence factory

        Args:
            user (User): user for auth
            circular (bool): True if sequence is circular False if not
            name (str): sequence name
            tags (List[Optional[str]]): tags for sequence filtering
            ncbi_id (str): sequence id from (https://www.ncbi.nlm.nih.gov/)

        Returns:
            SequenceModel: Sequence object
        """
        ncbi = [{"circular": circular,
                 "name": name,
                 "ncbiId": ncbi_id,
                 "tags": tags,
                 "type": "DNA"}]
        data = json.dumps({"circular": circular, "ncbis": ncbi, "tags": tags, "type": "DNA"})
        header = {"Content-type": "application/json",
                  "Accept": "application/json",
                  "Authorization": user.jwt}

        response = requests.post(f"{user.server}/sequence/import/ncbi", headers=header, data=data)
        data = validate_key_response(response=response, status_code=201, payload_key="items")
        return SequenceModel(**data[0])


class SequenceMethods:
    """SequenceMethods holds all sequence server methods"""

    @staticmethod
    def load_data(user: User, id: str, length: int, possiotion: int, sequence_length: int) -> str:
        """
        Return string with part of sequence

        Args:
            user (User): user for auth
            id (str): sequence id
            length (int): data string length
            possiotion (int): data start position
            sequence_length (int): sequence length for check

        Returns:
            str: String with part of sequence data
        """
        if possiotion >= 0 and 0 < length <= 1000 and possiotion + length <= sequence_length:
            header = {"Content-type": "application/json",
                      "Accept": "text/plain",
                      "Authorization": user.jwt}
            params = {"len": length, "pos": possiotion}

            response = requests.get(f"{user.server}/sequence/{id}/data", headers=header, params=params)
            return validate_text_response(response=response, status_code=200)
        else:
            Logger.error("Values out of range!")

    @staticmethod
    def delete(user: User, id: str) -> bool:
        """
        Delete sequence by id

        Args:
            user (User): user for auth
            id (str): sequence id

        Returns:
            bool: True if delete is successfull False if not
        """
        header = {"Content-type": "application/json",
                  "Accept": "*/*",
                  "Authorization": user.jwt}

        response = requests.delete(f"{user.server}/sequence/{id}", headers=header)
        if response.status_code == 204:
            return True
        return False

    @staticmethod
    def load_all(user: User, tags: List[Optional[str]]) -> Generator[SequenceModel, None, None]:
        """
        Load all sequences

        Args:
            user (User): user for auth
            tags (List[Optional[str]]): tags for filtering all sequences

        Returns:
            Generator[SequenceModel, None, None]: Sequence object generator
        """
        header = {"Content-type": "application/json",
                  "Accept": "application/json",
                  "Authorization": user.jwt}
        params = {"order": "ASC",
                  "requestForAll": "true",
                  "pageSize": "ALL",
                  "tags": tags}

        response = requests.get(f"{user.server}/sequence", headers=header, params=params)
        data = validate_key_response(response=response, status_code=200, payload_key="items")
        for record in data:
            yield SequenceModel(**record)

    @staticmethod
    def load_by_id(user: User, id: str) -> SequenceModel:
        """
        Delete sequence by id

        Args:
            user (User): user for auth
            id (str): sequence id

        Returns:
            SequenceModel: Sequence object
        """
        header = {"Content-type": "application/json",
                  "Accept": "application/json",
                  "Authorization": user.jwt}

        response = requests.get(f"{user.server}/sequence/{id}", headers=header)
        data = validate_key_response(response=response, status_code=200, payload_key="payload")
        return SequenceModel(**data)

    @staticmethod
    def nucleic_count(user: User, id: str) -> bool:
        """
        Run nucleic count of sequence by given id

        Args:
            user (User): user for auth
            id (str): sequence id

        Returns:
            bool: True if re-count is successfull False if not
        """
        header = {"Accept": "*/*",
                  "Authorization": user.jwt}

        response = requests.patch(f"{user.server}/sequence/{id}/nucleic-counts", headers=header)
        if response.status_code == 200:
            return True
        return False
