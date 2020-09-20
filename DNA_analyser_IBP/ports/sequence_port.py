# sequence_port.py

from typing import TYPE_CHECKING, Generator, List, Optional

from DNA_analyser_IBP.ports.port import Port

if TYPE_CHECKING:
    from DNA_analyser_IBP.models import Sequence, User


class SequencePort(Port):
    """
    Sequence port
    """

    def __init__(self, user: "User"):
        super().__init__(user=user)

    def create_text_sequence(
        self,
        *,
        circular: bool,
        data: str,
        name: str,
        tags: List[Optional[str]],
        nucleic_type: str,
    ) -> "Sequence":
        return self.adapter.sequence.create_text_sequence(
            circular=circular,
            data=data,
            name=name,
            tags=tags,
            nucleic_type=nucleic_type,
        )

    def create_file_sequence(
        self,
        *,
        circular: bool,
        path: str,
        name: str,
        tags: List[Optional[str]],
        nucleic_type: str,
        format: str,
    ) -> "Sequence":
        return self.adapter.sequence.create_file_sequence(
            circular=circular,
            path=path,
            name=name,
            tags=tags,
            nucleic_type=nucleic_type,
            format=format,
        )

    def create_ncbi_sequence(
        self,
        *,
        circular: bool,
        name: str,
        tags: List[Optional[str]],
        ncbi_id: str,
    ) -> "Sequence":
        return self.adapter.sequence.create_ncbi_sequence(
            circular=circular, name=name, tags=tags, ncbi_id=ncbi_id
        )

    def load_data(
        self, *, id: str, length: int, position: int, sequence_length: int
    ) -> str:
        return self.adapter.sequence.load_data(
            id=id, length=length, position=position, sequence_length=sequence_length
        )

    def load_all(
        self, *, tags: List[Optional[str]]
    ) -> "Generator[Sequence, None, None]":
        return self.adapter.sequence.load_all(tags=tags)

    def load_by_id(self, *, id: str) -> "Sequence":
        return self.adapter.sequence.load_by_id(id=id)

    def nucleic_count(self, id: str) -> bool:
        return self.adapter.sequence.nucleic_count(id=id)

    def delete(self, id: str) -> bool:
        return self.adapter.sequence.delete(id=id)
