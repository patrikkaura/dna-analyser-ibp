# g4hunter_caller.py


import json
from typing import Generator, List, Optional

import pandas as pd
import requests
import tenacity
from requests import Response

from DNA_analyser_IBP.adapters.base_adapter import BaseAdapter, BaseAnalyseAdapter
from DNA_analyser_IBP.adapters.validations import (
    validate_key_response,
    validate_text_response,
)
from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.models import RLoopr
from DNA_analyser_IBP.utils import generate_dataframe, join_url, login_required


class RLooprAdapter(BaseAdapter, BaseAnalyseAdapter):
    """
    G4Hunter factory used for generating analyse for given sequence
    """

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def create_analyse(
        self, id: str, tags: Optional[List[str]], riz_model: Optional[List[int]]
    ) -> RLoopr:
        """
        Send POST to /analyse/rloopr

        Args:
            id (str): sequence id
            tags (Optional[List[str]]): analyse tags
            riz_model (List[int): threshold for g4hunter algorithm recommended 1.2

        Returns:
            RLoopr: RLoopr model
        """
        header: dict = {
            "Accept": "application/json",
            "Authorization": self.user.jwt,
            "Content-type": "application/json",
        }
        data: str = json.dumps(
            {
                "sequence": id,
                "tags": tags or list(),
                "rizModel": riz_model or list(),
            }
        )
        response: Response = requests.post(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.RLOOPR),
            headers=header,
            data=data,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="payload"
        )

        return RLoopr(**data)

    @login_required
    def load_all(self, tags: List[Optional[str]]) -> Generator[RLoopr, None, None]:
        """
        Send GET to /analyse/rloopr

        Args:
            tags (List[Optional[str]]): filter tag for loading

        Returns:
            Generator[RLoopr, None, None], Exception: RLoopr object generator
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }
        params: dict = {
            "order": "ASC",
            "pageSize": "ALL",
            "tags": tags or list(),
            "requestForAll": "true",
        }

        response: Response = requests.get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.RLOOPR),
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="items"
        )

        for record in data:
            yield RLoopr(**record)

    @login_required
    def load_by_id(self, id: str) -> RLoopr:
        """
        Send GET to /analyse/rloopr/{id}/analyse

        Args:
            id (str): rloopr analyse id

        Returns:
            RLoopr: RLoopr object
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }

        response: Response = requests.get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.RLOOPR, id, "analysis"),
            headers=header,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="payload"
        )

        return RLoopr(**data)

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def delete(self, id: str) -> bool:
        """
        Send DELETE to /analyse/rloopr/{id}

        Args:
            id (str): rloopr analyse id
        Returns:
            bool: True if delete is successful False if not
        """
        header: dict = {
            "Accept": "*/*",
            "Authorization": self.user.jwt,
            "Content-type": "application/json",
        }

        response: Response = requests.delete(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.RLOOPR, id),
            headers=header,
        )

        if response.status_code == 204:
            return True
        return False

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def export_csv(self, id: str) -> str:
        """
        Send GET to /analyse/rloopr/{id}/rloopr.csv

        Args:
            id (str): rloopr analyse id

        Returns:
            str: csv file in string
        """
        header: dict = {"Accept": "text/plain", "Authorization": self.user.jwt}

        response: Response = requests.get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.RLOOPR, id, "rloopr.csv"),
            headers=header,
        )

        return validate_text_response(response=response, status_code=200)

    @login_required
    def load_result(self, id: str) -> pd.DataFrame:
        """
        Send GET to /analyse/rloopr/{id}/rloops

        Args:
            id (str): rloopr analyse id

        Returns:
            pd.DataFrame: DataFrame with RLoopr results
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }
        params: dict = {"order": "ASC", "requestForAll": "true", "pageSize": "ALL"}

        response: Response = requests.get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.RLOOPR, id, "rloops"),
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="payload"
        )

        return generate_dataframe(response=data)
