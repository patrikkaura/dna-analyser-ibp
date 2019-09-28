# g4hunter_caller.py
# !/usr/bin/env python3


import json
import requests
import pandas as pd
from typing import Generator, List, Union, Optional

from .user_caller import User
from .analyse_caller import AnalyseFactory, AnalyseModel
from ..utils import generate_dataframe, validate_key_response, validate_text_response


class G4HunterAnalyse(AnalyseModel):
    """G4Hunter analyse object finds guanine quadruplex in DNA/RNA sequence"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.result_count = kwargs.pop("resultCount")
        self.window_size = kwargs.pop("windowSize")
        self.threshold = kwargs.pop("threshold")
        self.frequency = kwargs.pop("frequency")

    def __str__(self):
        return f"G4Hunter {self.id} {self.title}"

    def __repr__(self):
        return f"<G4Hunter {self.id} {self.title}>"


class G4HunterAnalyseFactory(AnalyseFactory):
    """G4Hunter factory used for generating analyse for given sequence"""

    def create_analyse(self, user: User, id: str, tags: Optional[List[str]], threshold: float, window_size: int) -> Union[G4HunterAnalyse, Exception]:
        """
        G4hunter analyse factory
        :param user: user for auth
        :param id: sequence id
        :param tags: analyse tags
        :param threshold: threshold for g4hunter algorithm recommended 1.2
        :param window_size: window size for g4hunter algorithm recommended 25
        :return: G4Hunter object
        """
        # check range of parameters
        if 0.1 <= threshold <= 4 and 10 <= window_size <= 100:
            header = {"Content-type": "application/json",
                      "Accept": "application/json",
                      "Authorization": user.jwt}
            data = json.dumps({
                "sequence": id,
                "tags": tags or list(),
                "threshold": threshold,
                "windowSize": window_size})

            response = requests.post(f"{user.server}/analyse/g4hunter", headers=header, data=data)
            data = validate_key_response(response=response, status_code=201, payload_key="payload")
            return G4HunterAnalyse(**data)
        else:
            raise ValueError("Value window size or threshold out of range.")


def g4_delete_analyse(user: User, id: str) -> bool:
    """
    Delete analyse by id
    :param user: user for auth
    :param id: g4hunter analyse id
    :return: True if delete is successfull False if not
    """
    header = {"Content-type": "application/json",
              "Accept": "*/*",
              "Authorization": user.jwt}

    response = requests.delete(f"{user.server}/analyse/g4hunter/{id}", headers=header)
    if response.status_code == 204:
        return True
    return False


def g4_load_by_id(user: User, id: str) -> Union[G4HunterAnalyse, Exception]:
    """
    Load one g4hunter analyse by id
    :param user: user for auth
    :param id: g4hunter analyse id
    :return: G4Hunter object
    """
    header = {"Content-type": "application/json",
              "Accept": "application/json",
              "Authorization": user.jwt}

    response = requests.get(f"{user.server}/analyse/g4hunter/{id}", headers=header)
    data = validate_key_response(response=response, status_code=200, payload_key="payload")
    return G4HunterAnalyse(**data)


def g4_load_all(user: User, filter_tag: List[Optional[str]]) -> Union[Generator[G4HunterAnalyse, None, None], Exception]:
    """
    Load all g4hunter analyses
    :param user: user for auth
    :param filter_tag: filter tag for loading
    :return: G4Hunter object generator
    """
    header = {"Content-type": "application/json",
              "Accept": "application/json",
              "Authorization": user.jwt}
    params = {"order": "ASC",
              "requestForAll": "true",
              "pageSize": "ALL",
              "tags": filter_tag or list()}

    response = requests.get(f"{user.server}/analyse/g4hunter", headers=header, params=params)
    data = validate_key_response(response=response, status_code=200, payload_key="items")
    for record in data:
        yield G4HunterAnalyse(**record)


def g4_load_result(user: User, id: str) -> Union[pd.DataFrame, Exception]:
    """
    Load G4Hunter analyse result
    :param user: user for auth
    :param id: g4hunter analyse id
    :return: DataFrame with results
    """
    header = {"Content-type": "application/json",
              "Accept": "application/json",
              "Authorization": user.jwt}
    params = {"order": "ASC", "requestForAll": "true", "pageSize": "ALL"}

    response = requests.get(f"{user.server}/analyse/g4hunter/{id}/quadruplex", headers=header, params=params)
    data = validate_key_response(response=response, status_code=200, payload_key="items")
    return generate_dataframe(res=data)


def g4_export_csv(user: User, id: str, aggregate: bool = True) -> Union[str, Exception]:
    """
    Export G4Hunter results as csv output
    :param user: user for auth
    :param id: g4hunter analyse id
    :param aggregate: True if aggregate results else False
    :return: csv file in string
    """
    header = {"Accept": "text/plain", "Authorization": user.jwt}
    params = {"aggregate": "true" if aggregate else "false"}

    response = requests.get(f"{user.server}/analyse/g4hunter/{id}/quadruplex.csv", headers=header, params=params)
    csv_str = validate_text_response(response=response, status_code=200)
    return csv_str


def g4_load_heatmap(user: User, id: str, segment_count: int) -> Union[pd.DataFrame, Exception]:
    """
    Download heatmap data for G4Hunter analyse
    :param user: user for auth
    :param id: g4hunter analyse id
    :param segment_count: number of heatmap segments
    :return: DataFrame with segment data
    """
    header = {"Content-type": "application/json",
              "Accept": "application/json",
              "Authorization": user.jwt}
    params = {"segments": segment_count}

    response = requests.get(f"{user.server}/analyse/g4hunter/{id}/heatmap", headers=header, params=params)
    data = validate_key_response(response=response, status_code=200, payload_key="data")
    return pd.DataFrame(data=data)
