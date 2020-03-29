# utils.py
# !/usr/bin/env python3

import re
import os
import string
import pandas as pd
from functools import wraps
from requests import Response
from datetime import datetime
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
        print(f"{datetime.now()} [INFO]: {message}")

    @staticmethod
    def error(message: str) -> None:
        """
        Unified log messagge format [ERROR]

        Args:
            message (str): message to log
        """
        print(f"{datetime.now()} [ERROR]: {message}")


def normalize_name(name: str) -> str:
    """
    Normalize name e.g. filename|analyze name

    Args:
        name (str): string to normalize

    Returns:
        str: normalized string
    """
    valid_chars: list = "-_. %s%s" % (string.ascii_letters, string.digits)
    normalized_name: str = "".join(char for char in name if char in valid_chars)
    normalized_name = normalized_name.replace(" ", "_")
    return normalized_name


def exception_handler(fn):
    """Handle exception"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(f"{datetime.now()} [ERROR]: {str(e)}")

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
        data: pd.DataFrame = pd.DataFrame().from_records(
            response, columns=response[0].keys()
        )
        return data
    data: pd.DataFrame = pd.DataFrame(data=[response], columns=list(response.keys()))
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


def validate_key_response(
    response: Response, status_code: int, payload_key: Optional[str] = None
) -> dict:
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
        data: dict = response.json()
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
            row: str = row.strip()
            if row[0] == ">":  # pokud radek zacina >
                if not sequence_name:
                    sequence_name: str = row[1:]  # set new name
                elif row == "":
                    yield sequence_name, sequence_nucleic
                else:
                    yield sequence_name, sequence_nucleic
                    # set new name
                    sequence_name, sequence_nucleic = row[1:], str()
            else:
                sequence_nucleic += row
        yield sequence_name, sequence_nucleic


@exception_handler
def get_file_name(*, original_path: str, out_path: str, file_format: str) -> str:
    """
    Create new full path to given file
    Args:
        original_path (str): original file path
        out_path (str): output file path fro new file
        file_format (str): file format [e.g. csv]

    Returns:
        str: newly created file out path
    """
    path, file = os.path.split(original_path)  # split filename and path
    # new file name with given format
    new_file_name: str = f'{file.split(".")[0]}.{file_format}'
    # remove trailing slah or backslash
    out_path: str = (
        out_path[:-1] if out_path.endswith("/") or out_path.endswith("\\") else out_path
    )
    return f"{out_path}/{new_file_name}"
