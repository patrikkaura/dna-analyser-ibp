# batch_port.py

from typing import TYPE_CHECKING

from DNA_analyser_IBP.ports.port import Port

if TYPE_CHECKING:
    from DNA_analyser_IBP.models import Batch, User


class BatchPort(Port):
    """
    Batch port
    """

    def __init__(self, user: "User"):
        super().__init__(user=user)

    def get_batch_status(self, *, id: str, type: str) -> "Batch":
        return self.adapter.batch.get_batch_status(id=id, type=type)
