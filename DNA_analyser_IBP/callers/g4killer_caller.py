# g4killer_caller.py
# !/user/bin/env python 3


import json
import requests
import pandas as pd

from .analyse_caller import AnalyseFactory
from .user_caller import User
from ..utils import validate_key_response, Logger


class G4KillerAnalyse:
    """G4Killer analyse object destroy guanin quadruplex and lower G-score"""

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

        Returns:
            pd.DataFrame: dataframe with object data
        """
        data_frame = pd.DataFrame().from_records(self.__dict__, columns=self.__dict__.keys(), index=[0])
        return data_frame


class G4KillerAnalyseFactory(AnalyseFactory):
    """G4Killer factory used to generate analyse for given sequence string"""

    def create_analyse(self, user: User, sequence: str, threshold: float, complementary: bool) -> G4KillerAnalyse:
        """
        G4killer analyse factory

        Args:
            user (User): user for auth
            sequence (str): origin sequence for G4Killer procedure
            threshold (float): target g4hunter score in interval (0;4)
            complementary (bool): True if use for C sequence False for G sequence

        Returns:
            G4KillerAnalyse: G4KillerAnalyse object
        """
        # check range of parameters
        if 0 <= threshold <= 4:
            header = {"Content-type": "application/json",
                      "Accept": "application/json",
                      "Authorization": user.jwt}
            data = json.dumps({"sequence": sequence, "threshold": threshold, "onComplementary": "true" if complementary else "false"})

            response = requests.post(f"{user.server}/analyse/g4killer", headers=header, data=data)
            data = validate_key_response(response=response, status_code=201)
            return G4KillerAnalyse(**data)
        else:
            Logger.error("Value threshold out of interval (0;4)!")
