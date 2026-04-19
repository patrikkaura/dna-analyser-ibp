# rloopr_port.py

from typing import TYPE_CHECKING, Generator, List, Optional

from DNA_analyser_IBP.ports.port import Port

if TYPE_CHECKING:
    from pandas import DataFrame

    from DNA_analyser_IBP.models import RLoopr, User


class RlooprPort(Port):
    """
    Rloopr port
    """

    def __init__(self, user: "User"):
        super().__init__(user=user)

    def create_analyse(
        self,
        *,
        id: str,
        tags: Optional[List[str]],
        riz_model: Optional[List[int]],
    ) -> "RLoopr":
        return self.adapter.rloopr.create_analyse(id=id, tags=tags, riz_model=riz_model)

    def load_all(self, *, tags: List[Optional[str]]) -> Generator["RLoopr", None, None]:
        return self.adapter.rloopr.load_all(tags=tags)

    def load_by_id(self, *, id: str) -> "RLoopr":
        return self.adapter.rloopr.load_by_id(id=id)

    def delete(self, *, id: str) -> bool:
        return self.adapter.rloopr.delete(id=id)

    def export_csv(self, *, id: str, base_start: int = 0, base_end: int = 0) -> str:
        return self.adapter.rloopr.export_csv(id=id, base_start=base_start, base_end=base_end)


    def export_bedgraph(self, *, id: str, base_start: int = 0, base_end: int = 0) -> str:
        return self.adapter.rloopr.export_bedgraph(id=id, base_start=base_start, base_end=base_end)

    def load_result(self, *, id: str) -> "DataFrame":
        return self.adapter.rloopr.load_result(id=id)
