# utils.py
# !/usr/bin/env python3

import string
import re
import pandas as pd
from datetime import datetime
from functools import wraps
from requests import Response
from typing import Union, Optional


class Logger:
    """Simple unified logger"""

    @staticmethod
    def info(message: str) -> None:
        """
        Unified log messagge format [INFO]

        Args:
            message (str): message to log
        """
        print(f'{datetime.now()} [INFO]: {message}')

    @staticmethod
    def error(message: str) -> None:
        """
        Unified log messagge format [ERROR]

        Args:
            message (str): message to log
        """
        print(f'{datetime.now()} [ERROR]: {message}')


def normalize_name(name: str) -> str:
    """
    Normaliza name e.g. filename|analyze name

    Args:
        name (str): string to normalize

    Returns:
        str: normalized string
    """
    valid_chars = "-_. %s%s" % (string.ascii_letters, string.digits)
    normalized_name = ''.join(char for char in name if char in valid_chars)
    normalized_name = normalized_name.replace(' ', '_')
    return normalized_name


def exception_handler(fn):
    """Handle exception"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(f'{datetime.now()} [ERROR]: {str(e)}')

    return wrapper


def generate_dataframe(response: Union[dict, list]) -> pd.DataFrame:
    """
    Generate dataframe from given dict/list

    Args:
        response (Union[dict,list]): response dict|list

    Returns:
        pd.DataFrame: dataframe with response data
    """
    if isinstance(response, list):
        data = pd.DataFrame().from_records(response, columns=response[0].keys())
        return data
    data = pd.DataFrame(data=[response], columns=list(response.keys()))
    return data


def validate_email(email: str) -> bool:
    """
    Validate email address

    Args:
        email (str): test string

    Returns:
        bool: True is string is valid email else False
    """
    return bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email))


def validate_key_response(response: Response, status_code: int, payload_key: Optional[str] = None) -> dict:
    """
    Validate and convert JSON response to dictionary

    Args:
        response (Response): HTTP response
        status_code (int): HTTP status code
        payload_key (Optional[str]): payload key for validation

    Returns:
        dict: dictionary from response payload json
    """
    if response.status_code == status_code:
        data = response.json()
        if payload_key and data:
            if data[payload_key]:  # check if json and key exist
                return data[payload_key]
            else:
                raise ValueError(response.status_code, "Server returned no data")
        elif data:
            return data
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error or no data")


def validate_text_response(response: Response, status_code: int) -> str:
    """
    Validate and convert Text response to dictionary

    Args:
        response (Response): HTTP response
        status_code (int): HTTP status code

    Returns:
        str: string with response data
    """
    if response.status_code == status_code:
        if response.text:
            return response.text
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")


@exception_handler
def _multifasta_parser(*, path: str):
    """
    Parse Multifasta file and yield Fasta

    Args:
        path (str): system path to multifasta file
    """
    with open(path, "r") as multifasta:
        sequence_name, sequence_nucleic = str(), str()
        for index, row in enumerate(multifasta):
            row = row.strip()
            if row[0] == ">":  # pokud radek zacina >
                if not sequence_name:
                    sequence_name = row[1:]  # set new name
                elif row == "":
                    yield sequence_name, sequence_nucleic
                else:
                    yield sequence_name, sequence_nucleic
                    sequence_name, sequence_nucleic = row[1:], str()  # set new name
            else:
                sequence_nucleic += row
        yield sequence_name, sequence_nucleic
