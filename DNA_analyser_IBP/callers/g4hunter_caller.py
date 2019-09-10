# g4hunter_caller.py
# !/usr/bin/env python3
"""Library with G4hunter object.
Available classes:
- G4HunterAnalyse: G4hunter analyse object
- G4HunterAnalyseFactory: G4hunter analyse factory
"""

import json
from typing import Generator, List, Union
from .user_caller import User

import pandas as pd
import requests

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

    def create_analyse(
        self, user: User, id: str, tags: List[str], threshold: float, window_size: int
    ) -> Union[G4HunterAnalyse, Exception]:
        """G4hunter analyse factory
        
        Arguments:
            user {User} -- [user for auth]
            id {str} -- [sequence id for g4hunter analyse]
            tags {List[str]} -- [tags for analyse filtering]
            threshold {float} -- [threshold for g4hunter algorithm recommended 1.2]
            window_size {int} -- [window size for g4hunter algorithm recommended 25]
        
        Raises:
            ValueError: [if threshold not between 0.1 - 4 and window size 10 - 100]
        
        Returns:
            Union[G4HunterAnalyse, Exception] -- [G4Hunter object]
        """

        if (
            0.1 <= threshold <= 4 and 10 <= window_size <= 100
        ):  # check range of parameters
            header = {
                "Content-type": "application/json",
                "Accept": "application/json",
                "Authorization": user.jwt,
            }
            data = json.dumps(
                {
                    "sequences": [id],
                    "tags": tags,
                    "threshold": threshold,
                    "windowSize": window_size,
                }
            )
            
            response = requests.post(
                f"{user.server}/analyse/g4hunter", headers=header, data=data
            )
            data = validate_key_response(
                response=response, status_code=201, payload_key="items"
            )
            return G4HunterAnalyse(**data[0])
        else:
            raise ValueError("Value window size or threshold out of range.")


def g4_delete_analyse(user: User, id: str) -> bool:
    """Delete analyse by analyse id
    
    Arguments:
        user {User} -- [user for auth]
        id {str} -- [g4hunter analyse id]
    
    Returns:
        bool -- [True if delete is successfull False if not]
    """

    header = {
        "Content-type": "application/json",
        "Accept": "*/*",
        "Authorization": user.jwt,
    }
    
    response = requests.delete(f"{user.server}/analyse/g4hunter/{id}", headers=header)
    if response.status_code == 204:
        return True
    return False


def g4_load_by_id(user: User, id: str) -> Union[G4HunterAnalyse, Exception]:
    """List one g4hunter analyse by id
    
    Arguments:
        user {User} -- [user for auth]
        id {str} -- [g4hunter analyse id]
    
    Returns:
        Union[G4HunterAnalyse, Exception] -- [G4Hunter object]
    """

    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }
    
    response = requests.get(f"{user.server}/analyse/g4hunter/{id}", headers=header)
    data = validate_key_response(
        response=response, status_code=200, payload_key="payload"
    )
    return G4HunterAnalyse(**data)


def g4_load_all(
    user: User, filter_tag: List[str]
) -> Union[Generator[G4HunterAnalyse, None, None], Exception]:
    """List all g4hunter analyses
    
    Arguments:
        user {User} -- [user for auth]
        filter_tag {List[str]} -- [tags for filtering dataframe]
    
    Returns:
        Union[Generator[G4HunterAnalyse, None, None], Exception] -- [G4Hunter object generator]
    """
    
    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }
    params = {
        "order": "ASC",
        "requestForAll": "true",
        "pageSize": "ALL",
        "tags": filter_tag if filter_tag else None,
    }
   
    response = requests.get(
        f"{user.server}/analyse/g4hunter", headers=header, params=params
    )
    data = validate_key_response(
        response=response, status_code=200, payload_key="items"
    )
    for record in data:
        yield G4HunterAnalyse(**record)


def g4_load_result(user: User, id: str) -> Union[pd.DataFrame, Exception]:
    """Load g4hunter analyse results
    
    Arguments:
        user {User} -- [user for auth]
        id {str} -- [g4hunter analyse id]
    
    Returns:
        Union[pd.DataFrame, Exception] --  [G4Hunter result object]
    """
    
    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }
    params = {"order": "ASC", "requestForAll": "true", "pageSize": "ALL"}

    response = requests.get(
        f"{user.server}/analyse/g4hunter/{id}/quadruplex", headers=header, params=params
    )
    data = validate_key_response(
        response=response, status_code=200, payload_key="items"
    )
    return generate_dataframe(res=data)


def g4_export_csv(user: User, id: str, aggregate: bool = True) -> Union[str, Exception]:
    """Download csv output as text
    
    Arguments:
        user {User} -- [user for auth]
        id {str} -- [g4hunter analyse id]
    
    Keyword Arguments:
        aggregate {bool} -- [aggregate results = True else False (default: {True})]
    
    Returns:
        Union[str, Exception] -- [csv text format output]
    """

    header = {"Accept": "text/plain", "Authorization": user.jwt}
    params = {"aggregate": "true" if aggregate else "false"}

    response = requests.get(
        f"{user.server}/analyse/g4hunter/{id}/quadruplex.csv",
        headers=header,
        params=params,
    )
    csv_str = validate_text_response(response=response, status_code=200)
    return csv_str


def g4_load_heatmap(
    user: User, id: str, segment_count: int
) -> Union[pd.DataFrame, Exception]:
    """Download heatmap data for g4hunter analyse
    
    Arguments:
        user {User} -- [user for auth]
        id {str} -- [g4hunter analyse id]
        segment_count {int} -- [number of heatmap segments]
    
    Returns:
        Union[pd.DataFrame, Exception] -- [segmented heatmap data]
    """
    
    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }
    params = {"segments": segment_count}

    response = requests.get(
        f"{user.server}/analyse/g4hunter/{id}/heatmap", headers=header, params=params
    )
    data = validate_key_response(response=response, status_code=200, payload_key="data")
    return pd.DataFrame(data=data)
