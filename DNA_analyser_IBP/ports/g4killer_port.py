# g4killer_port.py

from typing import TYPE_CHECKING

from DNA_analyser_IBP.ports.port import Port

if TYPE_CHECKING:
    from DNA_analyser_IBP.models import G4Killer, User


class G4KillerPort(Port):
    """
    G4Killer port
    """

    def __init__(self, user: "User"):
        super().__init__(user=user)

    def create_analyse(
        self, *, sequence: str, threshold: float, complementary: bool
    ) -> "G4Killer":
        return self.adapter.g4killer.create_analyse(
            sequence=sequence, threshold=threshold, complementary=complementary
        )
