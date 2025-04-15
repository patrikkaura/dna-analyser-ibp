# batch_connector.py

import tenacity
from requests import Response, get

from DNA_analyser_IBP.adapters.base_adapter import BaseAdapter
from DNA_analyser_IBP.adapters.validations import validate_key_response
from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.models import Batch
from DNA_analyser_IBP.type import Types
from DNA_analyser_IBP.utils import join_url, login_required


class BatchAdapter(BaseAdapter):
    """
    Batch connector used in all models to check progress
    """

    def _get_batch_url(self, id: str, type: str) -> str:
        """
        Get batch enpoint url

        Args:
            id (str): id
            type (str): batch type

        Returns:
            str: batch url
        """
        if type == Types.SEQUENCE:
            return join_url(self.user.server, Config.BATCH_CONFIG.SEQUENCE, id)
        elif type == Types.G4HUNTER:
            return join_url(self.user.server, Config.BATCH_CONFIG.G4HUNTER, id)
        elif type == Types.RLOOPR:
            return join_url(self.user.server, Config.BATCH_CONFIG.RLOOPR, id)
        elif type == Types.ZDNA:
            return join_url(self.user.server, Config.BATCH_CONFIG.ZDNA, id)
        elif type == Types.CPG:
            return join_url(self.user.server, Config.BATCH_CONFIG.CPG, id)
        return str()

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def get_batch_status(self, id: str, type: str) -> Batch:
        """
        Send GET to SEQUENCE_BATCH_ENDPOINT

        Args:
            id (str): id
            type (str): batch type

        Returns:
            str: FINISH|FAILED
        """
        header: dict = {"Accept": "application/json", "Authorization": self.user.jwt}

        batch_url: str = self._get_batch_url(id=id, type=type)

        response: Response = get(
            batch_url,
            headers=header,
        )

        response_data: dict = validate_key_response(response=response, status_code=200)

        return Batch(**response_data)
