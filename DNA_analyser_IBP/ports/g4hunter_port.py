# g4hunter_port.py

from typing import TYPE_CHECKING, Generator, List, Optional

from DNA_analyser_IBP.ports.port import Port

if TYPE_CHECKING:
    from pandas import DataFrame

    from DNA_analyser_IBP.models import G4Hunter, User


class G4HunterPort(Port):
    """
    G4Hunter port
    """

    def __init__(self, user: "User"):
        super().__init__(user=user)

    def create_analyse(
        self,
        *,
        id: str,
        tags: Optional[List[str]],
        threshold: float,
        window_size: int,
    ) -> "G4Hunter":
        return self.adapter.g4hunter.create_analyse(
            id=id, tags=tags, threshold=threshold, window_size=window_size
        )

    def delete(self, *, id: str) -> bool:
        return self.adapter.g4hunter.delete(id=id)

    def load_by_id(self, *, id: str) -> "G4Hunter":
        return self.adapter.g4hunter.load_by_id(id=id)

    def load_all(
        self, *, tags: List[Optional[str]]
    ) -> "Generator[G4Hunter, None, None]":
        return self.adapter.g4hunter.load_all(tags=tags)

    def load_result(self, *, id: str) -> "DataFrame":
        return self.adapter.g4hunter.load_result(id=id)

    def export_csv(self, *, id: str, aggregate: bool = True) -> str:
        return self.adapter.g4hunter.export_csv(id=id, aggregate=aggregate)

    def load_heatmap(self, *, id: str, segments: int) -> "DataFrame":
        return self.adapter.g4hunter.load_heatmap(id=id, segments=segments)
