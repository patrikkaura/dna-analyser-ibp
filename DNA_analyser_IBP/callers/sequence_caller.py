# sequence_caller.py
# !/usr/bin/env python3

import abc
import json
import requests
import pandas as pd
from requests_toolbelt import MultipartEncoder
from typing import Generator, List, Union, Optional, Tuple

from .user_caller import User
from ..utils import validate_key_response, validate_text_response


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
        self.gc_count, self.nucleic_count = self.set_gc_count(kwargs.pop("nucleicCounts"))

    def __str__(self):
        return f"Sequence {self.id} {self.name} {self.type}"

    def __repr__(self):
        return f"<Sequence {self.id} {self.name} {self.type}>"

    def set_gc_count(self, nucleic_dict) -> Tuple[Optional[int], Optional[str]]:
        """
        Set gc count from nucleic count dict
        :return:
        """
        if nucleic_dict is not None:
            return int(nucleic_dict.get('C', 0)) + int(nucleic_dict.get('G', 0)), str(nucleic_dict)
        return None, None

    def get_dataframe(self) -> pd.DataFrame:
        """
        Return pandas dataframe for current object
        :return: dataframe with object data
        """
        data = pd.DataFrame().from_records(self.__dict__, columns=self.__dict__.keys(), index=[0])
        return data


class SequenceFactory(metaclass=abc.ABCMeta):
    """Abstract class for others sequence factories"""

    def __init__(self, **kwargs):
        self.sequence = self.create_sequence(**kwargs)

    @abc.abstractmethod
    def create_sequence(self, **kwargs) -> Union[SequenceModel, Exception]:
        """Creates sequence with different calls on Api"""
        raise NotImplementedError("You should implement this!")


class TextSequenceFactory(SequenceFactory):
    """Sequence factory used for generating sequence from raw text or text file"""

    def create_sequence(self, user: User, circular: bool, data: str, name: str, tags: List[Optional[str]], sequence_type: str) -> Union[SequenceModel, Exception]:
        """
        Text sequence factory
        :param user: user for auth
        :param circular: True if sequence is circular False if not
        :param data: string data with sequence
        :param name: sequence name
        :param tags: tags for sequence filtering
        :param sequence_type: string DNA / RNA
        :return: Sequence object
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
            "type": sequence_type})

        response = requests.post(f"{user.server}/sequence/import/text", headers=header, data=data)
        data = validate_key_response(response=response, status_code=201, payload_key="payload")
        return SequenceModel(**data)


class FileSequenceFactory(SequenceFactory):
    """Sequence factory used for generating sequence from file"""

    def create_sequence(self, user: User, circular: bool, file_path: str, name: str, tags: List[Optional[str]], sequence_type: str, format: str) -> Union[SequenceModel, Exception]:
        """
        File sequence factory
        :param user: user for auth
        :param circular: True if sequence is circular False if not
        :param file_path: absolute path to sequence file
        :param name: sequence name
        :param tags: tags for sequence filtering
        :param sequence_type: string DNA / RNA
        :param format: string FASTA / PLAIN
        :return: Sequence object
        """
        data = json.dumps({
            "circular": circular,
            "format": format,
            "name": name,
            "tags": tags,
            "type": sequence_type})
        multi_encoder = MultipartEncoder(fields={"json": data, "file": ("filename", open(file_path, "rb"))})
        header = {"Content-type": multi_encoder.content_type,
                  "Accept": "application/json",
                  "Authorization": user.jwt}

        response = requests.post(f"{user.server}/sequence/import/file", headers=header, data=multi_encoder)
        data = validate_key_response(response=response, status_code=201, payload_key="payload")
        return SequenceModel(**data)


class NCBISequenceFactory(SequenceFactory):
    """Sequence factory used for generating sequence from NCBI database"""

    def create_sequence(self, user: User, circular: bool, name: str, tags: List[Optional[str]], ncbi_id: str) -> Union[SequenceModel, Exception]:
        """
        NCBI sequence factory
        :param user: user for auth
        :param circular: True if sequence is circular False if not
        :param name: sequence name
        :param tags: tags for sequence filtering
        :param ncbi_id: sequence id from (https://www.ncbi.nlm.nih.gov/)
        :return: Sequence object
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


def seq_load_data(user: User, id: str, data_len: int, pos: int, seq_len: int) -> Union[str, Exception]:
    """
    Return string with part of sequence
    :param user: user for auth
    :param id: sequence id
    :param data_len: data string length
    :param pos: data start position
    :param seq_len: sequence length for check
    :return: String with part of sequence data
    """
    if pos >= 0 and 0 < data_len <= 1000 and pos + data_len <= seq_len:
        header = {"Content-type": "application/json",
                  "Accept": "text/plain",
                  "Authorization": user.jwt}
        params = {"len": data_len, "pos": pos}

        response = requests.get(f"{user.server}/sequence/{id}/data", headers=header, params=params)
        return validate_text_response(response=response, status_code=200)
    else:
        raise ValueError("Values out of range.")


def seq_delete(user: User, id: str) -> bool:
    """
    Delete sequence by id
    :param user: user for auth
    :param id: sequence id
    :return: True if delete is successfull False if not
    """
    header = {"Content-type": "application/json",
              "Accept": "*/*",
              "Authorization": user.jwt}

    response = requests.delete(f"{user.server}/sequence/{id}", headers=header)
    if response.status_code == 204:
        return True
    return False


def seq_load_all(user: User, filter_tag: List[Optional[str]]) -> Union[Generator[SequenceModel, None, None], Exception]:
    """
    Load all sequences
    :param user: user for auth
    :param filter_tag: tags for filtering all sequences
    :return: Sequence object generator]
    """
    header = {"Content-type": "application/json",
              "Accept": "application/json",
              "Authorization": user.jwt}
    params = {"order": "ASC",
              "requestForAll": "true",
              "pageSize": "ALL",
              "tags": filter_tag}

    response = requests.get(f"{user.server}/sequence", headers=header, params=params)
    data = validate_key_response(response=response, status_code=200, payload_key="items")
    for record in data:
        yield SequenceModel(**record)


def seq_load_by_id(user: User, id: str) -> Union[SequenceModel, Exception]:
    """
    Load sequence by id
    :param user: user for auth
    :param id: sequence id
    :return: Sequence object
    """
    header = {"Content-type": "application/json",
              "Accept": "application/json",
              "Authorization": user.jwt}

    response = requests.get(f"{user.server}/sequence/{id}", headers=header)
    data = validate_key_response(response=response, status_code=200, payload_key="payload")
    return SequenceModel(**data)
