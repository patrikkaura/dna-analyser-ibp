# p53_caller.py
# !/usr/bin/env python3
"""Library with P53 object.
Available classes:
- P53Analyse: P53 analyse object
- P53AnalyseFactory: P53 analyse factory
"""

import json
from typing import Union
from .user_caller import User

import pandas as pd
import requests

from .analyse_caller import AnalyseFactory
from ..utils import validate_key_response


class P53Analyse:
    """P53 analyse object finds p53 protein in DNA/RNA sequence."""

    def __init__(self, **kwargs):
        self.position = kwargs.pop("position")
        self.length = kwargs.pop("length")
        self.difference = kwargs.pop("difference")
        self.predictor = kwargs.pop("predictor")
        self.affinity = kwargs.pop("affinity")
        self.sequence = kwargs.pop("sequence")

    def __str__(self):
        return f"P53 {self.sequence}"

    def __repr__(self):
        return f"<P53 {self.sequence}>"

    def get_dataframe(self) -> pd.DataFrame:
        """Returns pandas dataframe for current object
        
        Returns:
            pd.DataFrame -- [pandas dataframe of analyse object]
        """
        data_frame = pd.DataFrame().from_records(
            self.__dict__, columns=self.__dict__.keys(), index=[0]
        )
        return data_frame


class P53AnalyseFactory(AnalyseFactory):
    """P53 factory used for generating analyse for given sequence."""

    def create_analyse(self, user: User, sequence: str) -> Union[P53Analyse, Exception]:
        """P53 analyse factory
        
        Arguments:
            user {User} -- [user for auth]
            sequence {str} -- [sequence string of length 20]
        
        Raises:
            ValueError: [if sequence len != 20]
        
        Returns:
            Union[P53Analyse, Exception] -- [P53Analyse object]
        """

        if len(sequence) == 20:
            header = {
                "Content-type": "application/json",
                "Accept": "application/json",
                "Authorization": user.jwt,
            }
            data = json.dumps({"sequence": sequence})
            response = requests.post(
                f"{user.server}/analyse/p53predictor/tool", headers=header, data=data
            )

            data = validate_key_response(
                response=response, status_code=200, payload_key="payload"
            )
            return P53Analyse(**data)
        else:
            raise ValueError("Sequence length must be 20 characters")
