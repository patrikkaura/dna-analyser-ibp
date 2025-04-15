# cpg_port.py

from typing import TYPE_CHECKING, Generator, List, Optional

from DNA_analyser_IBP.ports.port import Port

if TYPE_CHECKING:
    from pandas import DataFrame

    from DNA_analyser_IBP.models import CpG, User

class CpGPort(Port):
    """
    CpG Hunter Port
    """

    def __init__(self, user: "User"):
        super().__init__(user=user)

    def create_analyse(
        self,
        *,
        id: str,
        tags: Optional[List[str]],
        min_window_size: int,
        min_gc_percentage: float,
        min_obs_exp_cpg: float,
        min_island_merge_gap: int,
        second_nucleotide: str,
    ) -> "CpG":
        return self.adapter.cpg.create_analyse(
            id=id,
            tags=tags,
            min_window_size=min_window_size,
            min_gc_percentage=min_gc_percentage,
            min_obs_exp_cpg=min_obs_exp_cpg,
            min_island_merge_gap=min_island_merge_gap,
            second_nucleotide=second_nucleotide,
        )
    
    def load_all(self, *, tags: List[Optional[str]]) -> Generator["CpG", None, None]:
        return self.adapter.cpg.load_all(tags=tags)
    
    def load_by_id(self, *, id: str) -> "CpG":
        return self.adapter.cpg.load_by_id(id=id)
    
    def delete(self, *, id: str) -> bool:
        return self.adapter.cpg.delete(id=id)
    
    def export_csv(self, *, id: str) -> str:
        return self.adapter.cpg.export_csv(id=id)
    
    def load_result(self, *, id: str) -> "DataFrame":
        return self.adapter.cpg.load_result(id=id)