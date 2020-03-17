# batch_caller.py
# !/usr/bin/env python3

import requests
from .analyse_caller import AnalyseModel
from .sequence_caller import SequenceModel
from .user_caller import User


class BatchCaller:
    """Batch class used in all models to check progress"""

    def _process_response(response: object, success: bool) -> str:
        """Process response from batch caller
        
        Args:
            response (Object): Requests library response object
            success (bool): success condition given by bool or lambda
        
        Returns:
            str: batch status FINISH | FAILED
        """
        if response.status_code == 200 and response.text:
            batch_data: dict = response.json()
            return batch_data["status"]
        if success:
            return "FINISH"
        return "FAILED"

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
        header: dict = {"Accept": "application/json", "Authorization": user.jwt}

        response: object = requests.get(
            f"{user.server}/batch/cz.mendelu.dnaAnalyser.sequence.Sequence/{sequence.id}",
            headers=header,
        )
        success: bool = True if sequence.length is not None else False
        return BatchCaller._process_response(
            response=response, success=success
        )

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

        header: dict = {"Accept": "application/json", "Authorization": user.jwt}

        response: object = requests.get(
            f"{user.server}/batch/cz.mendelu.dnaAnalyser.analyse.g4hunter.G4Hunter/{analyse.id}",
            headers=header,
        )
        success: bool = True if analyse.finished is not None else False
        return BatchCaller._process_response(
            response=response, success=success
        )
