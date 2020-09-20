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
from DNA_analyser_IBP.models import G4Hunter
from DNA_analyser_IBP.utils import Logger, generate_dataframe, join_url, login_required


class G4HunterAdapter(BaseAdapter, BaseAnalyseAdapter):
    """
    G4Hunter factory used for generating analyse for given sequence
    """

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def create_analyse(
        self,
        id: str,
        tags: Optional[List[str]],
        threshold: float,
        window_size: int,
    ) -> G4Hunter:
        """
        Send POST to /analyse/g4hunter

        Args:
            id (str): sequence id
            tags (Optional[List[str]]): analyse tags
            threshold (float): threshold for g4hunter algorithm recommended 1.2
            window_size (int): window size for g4hunter algorithm recommended 25

        Returns:
            G4HunterModel: G4Hunter model
        """
        # check range of parameters
        if 0 <= threshold <= 4 and 10 <= window_size <= 100:
            header: dict = {
                "Accept": "application/json",
                "Authorization": self.user.jwt,
                "Content-type": "application/json",
            }
            data: str = json.dumps(
                {
                    "sequence": id,
                    "tags": tags or list(),
                    "threshold": threshold,
                    "windowSize": window_size,
                }
            )
            response: Response = requests.post(
                join_url(self.user.server, Config.ENDPOINT_CONFIG.G4HUNTER),
                headers=header,
                data=data,
            )
            data: dict = validate_key_response(
                response=response, status_code=201, payload_key="payload"
            )

            return G4Hunter(**data)
        else:
            Logger.error("Value window size or threshold out of range!")

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def delete(self, id: str) -> bool:
        """
        Send DELETE to /analyse/g4hunter/{id}

        Args:
            id (str): g4hunter analyse id
        Returns:
            bool: True if delete is successful False if not
        """
        header: dict = {
            "Accept": "*/*",
            "Authorization": self.user.jwt,
            "Content-type": "application/json",
        }

        response: Response = requests.delete(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.G4HUNTER, id),
            headers=header,
        )

        if response.status_code == 204:
            return True
        return False

    @login_required
    def load_by_id(self, id: str) -> G4Hunter:
        """
        Send GET to /analyse/g4hunter/{id}

        Args:
            id (str): g4hunter analyse id

        Returns:
            G4HunterModel: G4Hunter object
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }

        response: Response = requests.get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.G4HUNTER, id),
            headers=header,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="payload"
        )

        return G4Hunter(**data)

    @login_required
    def load_all(self, tags: List[Optional[str]]) -> Generator[G4Hunter, None, None]:
        """
        Send GET to /analyse/g4hunter

        Args:
            tags (List[Optional[str]]): filter tag for loading

        Returns:
            Generator[G4HunterModel, None, None], Exception: G4Hunter object generator
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
            join_url(self.user.server, Config.ENDPOINT_CONFIG.G4HUNTER),
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="items"
        )

        for record in data:
            yield G4Hunter(**record)

    @login_required
    def load_result(self, id: str) -> pd.DataFrame:
        """
        Send GET to /analyse/g4hunter/{id}/quadruplex

        Args:
            id (str): g4hunter analyse id

        Returns:
            pd.DataFrame: DataFrame with G4Hunter results
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }
        params: dict = {"order": "ASC", "requestForAll": "true", "pageSize": "ALL"}

        response: Response = requests.get(
            join_url(
                self.user.server, Config.ENDPOINT_CONFIG.G4HUNTER, id, "quadruplex"
            ),
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="items"
        )

        return generate_dataframe(response=data)

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def export_csv(self, id: str, aggregate: bool = True) -> str:
        """
        Send GET to /analyse/g4hunter/{id}/quadruplex.csv

        Args:
            id (str): g4hunter analyse id
            aggregate (bool): True if aggregate results else False

        Returns:
            str: csv file in string
        """
        header: dict = {"Accept": "text/plain", "Authorization": self.user.jwt}
        params: dict = {"aggregate": "true" if aggregate else "false"}

        response: Response = requests.get(
            join_url(
                self.user.server, Config.ENDPOINT_CONFIG.G4HUNTER, id, "quadruplex.csv"
            ),
            headers=header,
            params=params,
        )

        return validate_text_response(response=response, status_code=200)

    @login_required
    def load_heatmap(self, id: str, segments: int) -> pd.DataFrame:
        """
        Send GET to /analyse/g4hunter/{id}/heatmap

        Args:
            id (str): g4hunter analyse id
            segments (int): number of heatmap segments

        Returns:
            pd.DataFrame: dataFrame with heatmap data
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }
        params: dict = {"segments": segments}

        response = requests.get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.G4HUNTER, id, "heatmap"),
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="data"
        )

        heatmap: pd.DataFrame = pd.DataFrame(data=data)
        heatmap.rename(
            columns={"count": "PQS_count", "coverage": "PQS_coverage"}, inplace=True
        )

        return heatmap
