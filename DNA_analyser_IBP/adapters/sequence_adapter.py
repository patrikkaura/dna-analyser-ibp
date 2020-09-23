# sequence_connector.py

import json
from typing import Generator, List, Optional

import tenacity
from requests import Response, delete, get, patch, post
from requests_toolbelt import MultipartEncoder

from DNA_analyser_IBP.adapters.base_adapter import BaseAdapter
from DNA_analyser_IBP.adapters.validations import (
    validate_key_response,
    validate_text_response,
)
from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.models import Sequence
from DNA_analyser_IBP.utils import Logger, join_url, login_required


class SequenceAdapter(BaseAdapter):
    """
    Sequence connector used for sequence manipulation
    """

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def create_text_sequence(
        self,
        circular: bool,
        data: str,
        name: str,
        tags: List[Optional[str]],
        nucleic_type: str,
    ) -> Sequence:
        """
        Send POST to /sequence/import/text

        Args:
            circular (bool): True if sequence is circular False if not
            data (str): string data with sequence
            name (str): sequence name
            tags (List[Optional[str]]): tags for sequence filtering
            nucleic_type (str): string DNA|RNA

        Returns:
            SequenceModel: Sequence object
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }
        data: str = json.dumps(
            {
                "circular": circular,
                "data": data,
                "format": "PLAIN",
                "name": name,
                "tags": tags,
                "type": nucleic_type,
            }
        )

        response: Response = post(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.SEQUENCE, "import/text"),
            headers=header,
            data=data,
        )
        data: dict = validate_key_response(
            response=response, status_code=201, payload_key="payload"
        )

        return Sequence(**data)

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def create_file_sequence(
        self,
        circular: bool,
        path: str,
        name: str,
        tags: List[Optional[str]],
        nucleic_type: str,
        format: str,
    ) -> Sequence:
        """
        Send POST to /sequence/import/file

        Args:
            circular (bool): True if sequence is circular False if not
            path (str): absolute path to sequence file
            name (str): sequence name
            tags (List[Optional[str]]): tags for sequence filtering
            nucleic_type (str): string DNA|RNA
            format (str): string FASTA | PLAIN

        Returns:
            SequenceModel: Sequence object
        """
        data: str = json.dumps(
            {
                "circular": circular,
                "format": format,
                "name": name,
                "tags": tags,
                "type": nucleic_type,
            }
        )
        multi_encoder: MultipartEncoder = MultipartEncoder(
            fields={"json": data, "file": ("filename", open(path, "rb"))}
        )
        header: dict = {
            "Content-type": multi_encoder.content_type,
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }

        response: Response = post(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.SEQUENCE, "import/file"),
            headers=header,
            data=multi_encoder,
        )
        data: dict = validate_key_response(
            response=response, status_code=201, payload_key="payload"
        )

        return Sequence(**data)

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def create_ncbi_sequence(
        self,
        circular: bool,
        name: str,
        tags: List[Optional[str]],
        ncbi_id: str,
    ) -> Sequence:
        """
        Send POST to /sequence/import/ncbi

        Args:
            circular (bool): True if sequence is circular False if not
            name (str): sequence name
            tags (List[Optional[str]]): tags for sequence filtering
            ncbi_id (str): sequence id from (https://www.ncbi.nlm.nih.gov/)

        Returns:
            SequenceModel: Sequence object
        """
        ncbi: list = [
            {
                "circular": circular,
                "name": name,
                "ncbiId": ncbi_id,
                "tags": tags,
                "type": "DNA",
            }
        ]
        data: str = json.dumps(
            {"circular": circular, "ncbis": ncbi, "tags": tags, "type": "DNA"}
        )
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }
        response: Response = post(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.SEQUENCE, "import/ncbi"),
            headers=header,
            data=data,
        )
        data: dict = validate_key_response(
            response=response, status_code=201, payload_key="items"
        )

        return Sequence(**data[0])

    @login_required
    def load_data(
        self, id: str, length: int, position: int, sequence_length: int
    ) -> str:
        """
        Send GET to /sequence/{id}/data

        Args:
            id (str): sequence id
            length (int): data string length
            position (int): data start position
            sequence_length (int): sequence length for check

        Returns:
            str: String with part of sequence data
        """
        if (
            position >= 0
            and 0 < length <= 1000
            and position + length <= sequence_length
        ):
            header: dict = {
                "Content-type": "application/json",
                "Accept": "text/plain",
                "Authorization": self.user.jwt,
            }
            params: dict = {"len": length, "pos": position}

            response: Response = get(
                join_url(self.user.server, Config.ENDPOINT_CONFIG.SEQUENCE, id, "data"),
                headers=header,
                params=params,
            )

            return validate_text_response(response=response, status_code=200)
        else:
            Logger.error("Values out of range!")

    @login_required
    def load_all(self, tags: List[Optional[str]]) -> Generator[Sequence, None, None]:
        """
        Send GET /sequence

        Args:
            tags (List[Optional[str]]): tags for filtering all sequences

        Returns:
            Generator[SequenceModel, None, None]: Sequence object generator
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }
        params: dict = {
            "order": "ASC",
            "requestForAll": "true",
            "pageSize": "ALL",
            "tags": tags,
        }

        response: Response = get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.SEQUENCE),
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="items"
        )

        for record in data:
            yield Sequence(**record)

    @login_required
    def load_by_id(self, id: str) -> Sequence:
        """
        Send GET /sequence/id

        Args:
            id (str): sequence id

        Returns:
            SequenceModel: Sequence object
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": self.user.jwt,
        }

        response: Response = get(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.SEQUENCE, id),
            headers=header,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="payload"
        )

        return Sequence(**data)

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def nucleic_count(self, id: str) -> bool:
        """
        Send PATCH to /sequence/{id}/nucleic-counts

        Args:
            id (str): sequence id

        Returns:
            bool: True if re-count is successful False if not
        """
        header: dict = {"Accept": "*/*", "Authorization": self.user.jwt}

        response: Response = patch(
            join_url(
                self.user.server, Config.ENDPOINT_CONFIG.SEQUENCE, id, "nucleic-counts"
            ),
            headers=header,
        )

        if response.status_code == 200:
            return True
        return False

    @tenacity.retry(wait=Config.TENACITY_CONFIG.WAIT, stop=Config.TENACITY_CONFIG.STOP)
    @login_required
    def delete(self, id: str) -> bool:
        """
        Send DELETE to /sequence/id

        Args:
            id (str): sequence id

        Returns:
            bool: True if delete is successful False if not
        """
        header: dict = {
            "Accept": "*/*",
            "Authorization": self.user.jwt,
            "Content-type": "application/json",
        }

        response: Response = delete(
            join_url(self.user.server, Config.ENDPOINT_CONFIG.SEQUENCE, id),
            headers=header,
        )

        if response.status_code == 204:
            return True
        return False
