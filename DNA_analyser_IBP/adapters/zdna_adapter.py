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
from DNA_analyser_IBP.models import ZDna
from DNA_analyser_IBP.utils import Logger, generate_dataframe, join_url, login_required


class ZDnaAdapter(BaseAdapter, BaseAnalyseAdapter):
    """
    Z-DNA factory used for generating analyse for given sequence
    """

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def create_analyse(
            self,
            id: str,
            tags: Optional[List[str]],
            min_sequence_size: int,
            model: Optional[List[str]],
            GC_score: float,
            GTAC_score: float,
            AT_score: float,
            oth_score: float,
            min_score_percentage: float
            ) -> ZDna:
        """
        id (str): sequence id
        tags (Optional[List[str]]): analyse tags
        min_sequence_size (int): minimal length of sequences searched, minimum 6, default 10
        model (Optional[List[str]]): choice of models influencing the score parameters
        GC_score (float): score for the GC pair, minimum 0.1, defaults: 25 (model 1), 2 (model 2)
        GTAC_score (float): score for the GT or AC pair, minimum 0, defaults: 3 (model 1), 1 (model 2)
        AT_score (float): score for the AT pair, minimum 0, defaults: 0 (model 1), 0.5 (model 2)
        min_score_perc (float): minimum score for the searched Z-DNA window (input values as percentages), minimum: 12, defaults: 12 (model 1), 50 (model 2)
        """
        conditions: List[bool] = (
            min_sequence_size >= 6,
            GC_score >= 0.1,
            GTAC_score >= 0,
            AT_score >= 0,
            min_score_percentage >= 12
        )

        if all(conditions):
            header: dict = {
                "Accept": "application/json",
                "Authorization": self.user.jwt,
                "Content-type": "application/json",
            }

            data: str = json.dumps(
                {
                    "sequence": id,
                    "tags": tags or list(),
                    "minSequenceSize": min_sequence_size,
                    "selectedModel": model or list(),
                    "score_gc": GC_score,
                    "score_gtac": GTAC_score,
                    "score_at": AT_score,
                    "score_oth": oth_score,
                    "threshold": min_score_percentage,
                }
            )

            response: Response = requests.post(
                join_url(self.user.server, Config.ENDPOINT_CONFIG.ZDNA),
                headers=header,
                data=data,
            )

            data: dict = validate_key_response(
                response=response, status_code=200, payload_key="payload"
            )

            return ZDna(**data)
        else:
            Logger.error("Parameters out of permitted range!")

    @login_required
    def load_all(self, tags: List[Optional[str]]) -> Generator[ZDna, None, None]:
        """
        Send GET to /analyse/zdna

        Args:
            tags (List[Optional[str]]): filter tag for loading

        Returns:
            Generator[ZDna, None, None], Exception: ZDna object generator
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
            join_url(self.user.server, Config.ENDPOINT_CONFIG.ZDNA),
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="items"
        )

        for record in data:
            yield ZDna(**record)

    @login_required
    def load_by_id(self, id: str) -> ZDna:
        """
        Send GET to /analyse/zdna/{id}/analyse

        Args:
            id (str): Z-DNA analyse id

        Returns:
            ZDna: ZDna object
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }

        response: Response = requests.get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.ZDNA, id, "analysis"),
            headers=header,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="payload"
        )

        return ZDna(**data)

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def delete(self, id: str) -> bool:
        """
        Send DELETE to /analyse/zdna/{id}

        Args:
            id (str): Z-DNA analyse id
        Returns:
            bool: True if delete is successful False if not
        """
        header: dict = {
            "Accept": "*/*",
            "Authorization": self.user.jwt,
            "Content-type": "application/json",
        }

        response: Response = requests.delete(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.ZDNA, id),
            headers=header,
        )

        if response.status_code == 204:
            return True
        return False

    @login_required
    def load_result(self, id: str) -> pd.DataFrame:
        """
        Send GET to /analyse/zdna/{id}/zdnas

        Args:
            id (str): Z-DNA analyse id

        Returns:
            pd.DataFrame: DataFrame with ZDna results
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }
        params: dict = {"order": "ASC", "requestForAll": "true", "pageSize": "ALL"}

        response: Response = requests.get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.ZDNA, id, "zdnas"),
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="items"
        )

        return generate_dataframe(response=data)

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def export_csv(self, id: str) -> str:
        """
        Send GET to /analyse/zdna/{id}/zdna.csv

        Args:
            id (str): Z-DNA analyse id

        Returns:
            str: csv file in string
        """
        header: dict = {"Accept": "text/plain", "Authorization": self.user.jwt}

        response: Response = requests.get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.ZDNA, id, "zdna.csv"),
            headers=header,
        )

        return validate_text_response(response=response, status_code=200)

    @login_required
    def load_heatmap(self, id: str, segments: int) -> pd.DataFrame:
        """
        Send GET to /analyse/zdna/{id}/heatmap

        Args:
            id (str): Z-DNA analyse id
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
            join_url(self.user.server, Config.ENDPOINT_CONFIG.ZDNA, id, "heatmap"),
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="data"
        )

        heatmap: pd.DataFrame = pd.DataFrame(data=data)
        heatmap.rename(
            columns={"count": "Z-DNA_count", "coverage": "Z-DNA_coverage"}, inplace=True
        )

        return heatmap
