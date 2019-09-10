# utils.py
# !/usr/bin/env python3
"""
Module with support functions used in multiple files.
"""

import pandas as pd
import re
from requests import Response


def generate_dataframe(res: dict or list) -> pd.DataFrame:
    """Generate dataframe for given dict / list
    
    Arguments:
        res {dictorlist} -- [response dict / list]
    
    Returns:
        pd.DataFrame -- [dataframe with response data]
    """

    if isinstance(res, list):
        data = pd.DataFrame().from_records(res, columns=res[0].keys())
        return data
    data = pd.DataFrame(data=[res], columns=list(res.keys()))
    return data


def validate_email(email: str) -> bool:
    """[summary]
    
    Arguments:
        value {str} -- [email string]
    
    Returns:
        bool -- [if True email is valid else False]
    """

    return bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email))


def validate_key_response(
        response: Response, status_code: int, payload_key: str = None
) -> dict:
    """Validate and convert json response to dict
    
    Arguments:
        response {Response} -- [resposne data from requests]
        status_code {int} -- [response status code]
    
    Keyword Arguments:
        payload_key {str} -- [dict key for data] (default: {None})
    
    Raises:
        ValueError: [no data in payload key]
        ValueError: [no payload key or data]
        ConnectionError: [wrong status code]
    
    Returns:
        dict -- [dict from json]
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
    """Validate text data and convert to str
    
    Arguments:
        response {Response} -- [resposne data from requests]
        status_code {int} -- [response status code]
    
    Raises:
        ValueError: [no data in payload text]
        ConnectionError: [wrong status code]
    
    Returns:
        str -- [string with data]
    """

    if response.status_code == status_code:
        if response.text:
            return response.text
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")
