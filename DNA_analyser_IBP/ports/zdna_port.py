# zdna_port.py

from typing import TYPE_CHECKING, Generator, List, Optional

from DNA_analyser_IBP.ports.port import Port

if TYPE_CHECKING:
    from pandas import DataFrame

    from DNA_analyser_IBP.models import ZDna, User


class ZDnaPort(Port):
    """
    Z-Dna hunter port
    """

    def __init__(self, user: "User"):
        super().__init__(user=user)

    def create_analyse(
        self,
        *,
        id: str,
        tags: Optional[List[str]],
        min_sequence_size: int,
        model: Optional[List[str]],
        GC_score: float,
        GTAC_score: float,
        AT_score: float,
        oth_score: float,
        min_score_percentage: float
    ) -> "ZDna":
        return self.adapter.zdna.create_analyse(
            id=id, 
            tags=tags, 
            min_sequence_size=min_sequence_size,
            model = model,
            GC_score = GC_score,
            GTAC_score = GTAC_score,
            AT_score = AT_score,
            oth_score = oth_score,
            min_score_percentage = min_score_percentage,
        )
    
    def delete(self, *, id: str) -> bool:
        return self.adapter.zdna.delete(id=id)

    def load_by_id(self, *, id: str) -> "ZDna":
        return self.adapter.zdna.load_by_id(id=id)

    def load_all(
        self, *, tags: List[Optional[str]]
    ) -> "Generator[ZDna, None, None]":
        return self.adapter.zdna.load_all(tags=tags)
    
    def load_result(self, *, id: str) -> "DataFrame":
        return self.adapter.zdna.load_result(id=id)

    def export_csv(self, *, id: str) -> str:
        return self.adapter.zdna.export_csv(id=id)

    def load_heatmap(self, *, id: str, segments: int) -> "DataFrame":
        return self.adapter.zdna.load_heatmap(id=id, segments=segments)