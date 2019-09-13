# p53_caller.py
# !/usr/bin/env python3


import json
import pandas as pd
import requests
from typing import Union

from .user_caller import User
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
        """
        Return pandas dataframe for current object
        :return: dataframe with object data
        """
        data_frame = pd.DataFrame().from_records(self.__dict__, columns=self.__dict__.keys(), index=[0])
        return data_frame


class P53AnalyseFactory(AnalyseFactory):
    """P53 factory used for generating analyse for given sequence."""

    def create_analyse(self, user: User, sequence: str) -> Union[P53Analyse, Exception]:
        """
        P53 analyse factory
        :param user: user for auth
        :param sequence: sequence string of lenght 20
        :return: P53Analyse object
        """
        # check if sequence lenght is exactly 20 chars
        if len(sequence) == 20:
            header = {"Content-type": "application/json",
                      "Accept": "application/json",
                      "Authorization": user.jwt}
            data = json.dumps({"sequence": sequence})

            response = requests.post(f"{user.server}/analyse/p53predictor/tool", headers=header, data=data)
            data = validate_key_response(response=response, status_code=200, payload_key="payload")
            return P53Analyse(**data)
        else:
            raise ValueError("Sequence length must be 20 characters")
