# batch_caller.py
# !/usr/bin/env python3

import requests
from .analyse_caller import AnalyseModel
from .sequence_caller import SequenceModel
from .user_caller import User


class BatchCaller:
    """Batch class used in all models to check progress"""

    @staticmethod
    def get_sequence_batch_status(sequence: SequenceModel, user: User) -> str:
        """
        Return sequence batch status (CREATED, WAITING, RUNNING, FINISH, FAILED)

        Args:
            sequence (SequenceModel): Sequence object
            user (User): user for auth

        Returns:
            str: FINISH|FAILED
        """
        header = {"Accept": "application/json", "Authorization": user.jwt}

        response = requests.get(f"{user.server}/batch/cz.mendelu.dnaAnalyser.sequence.Sequence/{sequence.id}", headers=header)
        if response.status_code == 200 and response.text:
            batch_data = response.json()
            return batch_data["status"]
        if sequence.length is not None:
            return "FINISH"
        return "FAILED"

    @staticmethod
    def get_analyse_batch_status(analyse: AnalyseModel, user: User) -> str:
        """
        Return sequence batch status (CREATED, WAITING, RUNNING, FINISH, FAILED)

        Args:
            analyse (AnalyseModel): Analyse object
            user (User): user for auth

        Returns:
            str: FINISH|FAILED
        """

        header = {"Accept": "application/json", "Authorization": user.jwt}

        response = requests.get(f"{user.server}/batch/cz.mendelu.dnaAnalyser.analyse.g4hunter.G4Hunter/{analyse.id}", headers=header)
        if response.status_code == 200 and response.text:
            batch_data = response.json()
            return batch_data["status"]
        if analyse.finished is not None:
            return "FINISH"
        return "FAILED"
