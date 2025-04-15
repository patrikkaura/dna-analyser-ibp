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
from DNA_analyser_IBP.models import CpG
from DNA_analyser_IBP.utils import Logger, generate_dataframe, join_url, login_required


class CpGAdapter(BaseAdapter, BaseAnalyseAdapter):
    """
    G4Hunter factory used for generating analyse for given sequence
    """

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def create_analyse(
        self,
        id: str,
        tags: Optional[List[str]],
        min_window_size: int,
        min_gc_percentage: float,
        min_obs_exp_cpg: float,
        min_island_merge_gap: int,
        second_nucleotide: str,
    ) -> CpG:
        """
        Send POST to /analyse/cpg

        Args:
            id (str): sequence id
            tags (Optional[List[str]]): analyse tags
            min_window_size (int): smallest bp window size that can be considered a window, default: 200, min: 10, max: 10 000
            min_gc_percentage (float): minimum required content fraction between C and "X" (second nucleotide), default: 0.5, min: 0, max: 1
            min_obs_exp_cpg (float): minimum required fraction of observed to expected CpG dinucleotides, default: 0.6, min: 0, max: 1
            min_island_merge_gap (int): smallest bp gap between two islands, which will cause them to merge into one, default: 100, min: 10, max: 10 000
            second nucleotide (str): the second nucleotide of the island, which can be "G", "A", "T", or "C", default: "G"

        Returns:
            G4HunterModel: G4Hunter model
        """

        conditions: List[bool] = [
            10 <= min_window_size <= 1E4,
            0 <= min_gc_percentage <= 1,
            0 <= min_obs_exp_cpg <= 1,
            10 <= min_island_merge_gap <= 1E4,
            second_nucleotide in ["G", "A", "T", "C"],
        ]

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
                    "minWindowSize": min_window_size,
                    "minGcPercentage": min_gc_percentage,
                    "minObservedToExpectedCpG": min_obs_exp_cpg,
                    "minIslandMergeGap": min_island_merge_gap,
                    "firstNucleotide": "C",
                    "secondNucleotide": second_nucleotide,
                }
            )
            response: Response = requests.post(
                join_url(self.user.server, Config.ENDPOINT_CONFIG.CPG),
                headers=header,
                data=data,
            )
            data: dict = validate_key_response(
                response=response, status_code=200, payload_key="payload"
            )

            return CpG(**data)
        else:
            Logger.error("Parameters out of permitted range!")

    def load_all(self, tags: List[Optional[str]]) -> Generator[CpG, None, None]:
        """
        Send GET to /analyse/cpg

        Args:
            tags (List[Optional[str]]): filter tag for loading

        Returns:
            Generator[CpG, None, None], Exception: CpG object generator
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
            join_url(self.user.server, Config.ENDPOINT_CONFIG.CPG),
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="items"
        )

        for record in data:
            yield CpG(**record)

    @login_required
    def load_by_id(self, id: str) -> CpG:
        """
        Send GET to /analyse/cpg/{id}/analyse

        Args:
            id (str): cpg analyse id

        Returns:
            RLoopr: CpG object
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }

        response: Response = requests.get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.CPG, id, "analysis"),
            headers=header,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="payload"
        )

        return CpG(**data)
    
    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def delete(self, id: str) -> bool:
        """
        Send DELETE to /analyse/cpg/{id}

        Args:
            id (str): cpg analyse id
        Returns:
            bool: True if delete is successful False if not
        """
        header: dict = {
            "Accept": "*/*",
            "Authorization": self.user.jwt,
            "Content-type": "application/json",
        }

        response: Response = requests.delete(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.CPG, id),
            headers=header,
        )

        if response.status_code == 204:
            return True
        return False
    
    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def export_csv(self, id: str) -> str:
        """
        Send GET to /analyse/cpg/{id}/cpg.csv

        Args:
            id (str): cpg analyse id

        Returns:
            str: csv file in string
        """
        header: dict = {"Accept": "text/plain", "Authorization": self.user.jwt}

        response: Response = requests.get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.CPG, id, "cpg.csv"),
            headers=header,
        )

        return validate_text_response(response=response, status_code=200)
    
    @login_required
    def load_result(self, id: str) -> pd.DataFrame:
        """
        Send GET to /analyse/cpg/{id}/cpg

        Args:
            id (str): cpg analyse id

        Returns:
            pd.DataFrame: DataFrame with CpG results
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }
        params: dict = {"order": "ASC", "requestForAll": "true", "pageSize": "ALL"}

        response: Response = requests.get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.CPG, id, "cpg"),
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="items"
        )

        return generate_dataframe(response=data)
