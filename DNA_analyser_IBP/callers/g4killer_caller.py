# g4killer_caller.py
# !/user/bin/env python 3


import json
import requests
import pandas as pd
from typing import Union

from .analyse_caller import AnalyseFactory
from .user_caller import User
from ..utils import validate_key_response


# TODO: fix same as on website

class G4KillerAnalyse:
    """G4Killer analyse object desctroi guanin quadruplex and change gscore"""

    def __init__(self, **kwargs):
        self.origin_score = kwargs.pop("originScore")
        self.target_threshold = kwargs.pop("targetThreshold")
        self.origin_sequence = kwargs.pop("originSequence")
        self.mutation_sequences = kwargs.pop("mutationSequences")
        self.mutation_score = kwargs.pop("mutationScore")
        self.change_count = kwargs.pop("changeCount")
        self.mutation_variants = kwargs.pop("mutationVariants")
        self.on_complementary = kwargs.pop("onComplementary")

    def __str__(self):
        return f"G4Killer {self.origin_sequence} {self.mutation_sequences[0]}"

    def __repr__(self):
        return f"<G4Killer {self.origin_sequence} {self.mutation_sequences[0]}>"

    def get_dataframe(self) -> pd.DataFrame:
        """
        Return pandas dataframe for current object
        :return: dataframe with object data
        """
        data_frame = pd.DataFrame().from_records(self.__dict__, columns=self.__dict__.keys(), index=[0])
        return data_frame


class G4KillerAnalyseFactory(AnalyseFactory):
    """G4Killer factory used to generate analyse for given sequence string"""

    def create_analyse(self, user: User, origin_sequence: str, threshold: float, on_complementary: bool) -> Union[G4KillerAnalyse, Exception]:
        """
        G4killer analyse factory
        :param user: user for auth
        :param origin_sequence: origin sequence for killer procedure
        :param threshold: target g4hunter score
        :param on_complementary: True if use for C sequence False for G sequence
        :return: G4Killer object
        """
        # check range of parameters
        if 0 <= threshold <= 4:
            header = {"Content-type": "application/json",
                      "Accept": "application/json",
                      "Authorization": user.jwt}
            data = json.dumps({"sequence": origin_sequence, "threshold": threshold, "onComplementary": "true" if on_complementary else "false"})

            response = requests.post(f"{user.server}/analyse/g4killer", headers=header, data=data)
            data = validate_key_response(response=response, status_code=201)
            return G4KillerAnalyse(**data)
        else:
            raise ValueError("Value threshold out of range")
