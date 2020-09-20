# p53_adapter.py


import json

from requests import Response, post

from DNA_analyser_IBP.adapters.base_adapter import BaseAdapter, BaseAnalyseAdapter
from DNA_analyser_IBP.adapters.validations import validate_key_response
from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.models import P53
from DNA_analyser_IBP.utils import Logger, join_url, login_required


class P53Adapter(BaseAdapter, BaseAnalyseAdapter):
    """
    P53 connector used for generating analyse for given sequence
    """

    @login_required
    def create_analyse(self, sequence: str) -> P53:
        """
        Send POST to /analyse/p53predictor/tool

        Args:
            sequence (str): sequence string of length 20

        Returns:
            P53Model: P53Model object
        """
        # check if sequence length is exactly 20 chars
        if sequence and len(sequence) == 20:
            header: dict = {
                "Authorization": self.user.jwt,
                "Accept": "application/json",
                "Content-type": "application/json",
            }
            data: str = json.dumps({"sequence": sequence})

            response: Response = post(
                join_url(self.user.server, Config.ENDPOINT_CONFIG.P53),
                headers=header,
                data=data,
            )
            response_data: dict = validate_key_response(
                response=response, status_code=200, payload_key="payload"
            )

            return P53(**response_data)
        else:
            Logger.error("Sequence length must be exactly 20 characters!")
