# utils.py
# !/usr/bin/env python3


import re
import pandas as pd
from requests import Response
from typing import Union, Optional


def generate_dataframe(res: Union[dict, list]) -> pd.DataFrame:
    """
    Generate dataframe from given dict/list
    :param res: response dict/list
    :return: dataframe with response data
    """
    if isinstance(res, list):
        data = pd.DataFrame().from_records(res, columns=res[0].keys())
        return data
    data = pd.DataFrame(data=[res], columns=list(res.keys()))
    return data


def validate_email(email: str) -> bool:
    """
    Validate email address
    :param email: tested string
    :return: True is string is valid email else False
    """
    return bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email))


def validate_key_response(response: Response, status_code: int, payload_key: Optional[str] = None) -> dict:
    """
    Validate and convert JSON response to dictionary
    :param response: HTTP response
    :param status_code: HTTP status code
    :param payload_key: payload key for validation
    :return: dictionary from payload json
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
    :param response: HTTP response
    :param status_code: HTTP status code
    :return: string with response
    """
    if response.status_code == status_code:
        if response.text:
            return response.text
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")
