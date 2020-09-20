# validations.py


from typing import Dict, Optional, Union

from requests import Response


class ApiConnectionError(Exception):
    pass


class ApiEmptyResponse(Exception):
    pass


def validate_key_response(
    response: Response, status_code: int, payload_key: Optional[str] = None
) -> Union[Exception, Dict]:
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
            if data[payload_key]:
                return data[payload_key]
            else:
                raise ApiEmptyResponse(response.status_code, "Server returned no data")
        elif data:
            return data
        else:
            raise ApiEmptyResponse(response.status_code, "Server returned no data")
    else:
        raise ApiConnectionError(
            response.status_code, "Server error or returned no data"
        )


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
            raise ApiEmptyResponse(response.status_code, "Server returned no data")
    else:
        raise ApiConnectionError(response.status_code, "Server error")
