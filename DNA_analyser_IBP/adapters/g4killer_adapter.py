# g4killer_adapter.py


import json

from requests import Response, post

from DNA_analyser_IBP.adapters.base_adapter import BaseAdapter, BaseAnalyseAdapter
from DNA_analyser_IBP.adapters.validations import validate_key_response
from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.models import G4Killer
from DNA_analyser_IBP.utils import Logger, join_url, login_required


class G4KillerAdapter(BaseAdapter, BaseAnalyseAdapter):
    """
    G4Killer connector used to generate analyse for given sequence string
    """

    @login_required
    def create_analyse(
        self, sequence: str, threshold: float, complementary: bool
    ) -> G4Killer:
        """
        Send POST to /analyse/g4killer

        Args:
            sequence (str): origin sequence for G4Killer procedure
            threshold (float): target g4hunter score in interval <0;4>
            complementary (bool): True if use for C sequence False for G sequence

        Returns:
            G4KillerModel: G4KillerModel object
        """
        # check range of parameters
        if sequence and (0 < len(sequence) <= 200) and (0 <= threshold <= 4):
            header: dict = {
                "Authorization": self.user.jwt,
                "Accept": "application/json",
                "Content-type": "application/json",
            }
            data: str = json.dumps(
                {
                    "sequence": sequence,
                    "threshold": threshold,
                    "onComplementary": "true" if complementary else "false",
                }
            )

            response: Response = post(
                join_url(self.user.server, Config.ENDPOINT_CONFIG.G4KILLER),
                headers=header,
                data=data,
            )
            response_data: dict = validate_key_response(
                response=response, status_code=201
            )
            return G4Killer(**response_data)
        else:
            Logger.error(
                "Value threshold out of interval (0;4) and sequence has to be in interval (0;200)!"
            )
