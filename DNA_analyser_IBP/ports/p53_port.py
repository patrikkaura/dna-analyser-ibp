# p53_port.py

from typing import TYPE_CHECKING

from DNA_analyser_IBP.ports.port import Port

if TYPE_CHECKING:
    from DNA_analyser_IBP.models import P53, User


class P53Port(Port):
    """
    P53 port
    """

    def __init__(self, user: "User"):
        super().__init__(user=user)

    def create_analyse(self, *, sequence: str) -> "P53":
        return self.adapter.p53.create_analyse(sequence=sequence)
