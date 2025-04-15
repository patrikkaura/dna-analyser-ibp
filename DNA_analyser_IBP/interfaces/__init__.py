# __init__.py

from typing import TYPE_CHECKING

from DNA_analyser_IBP.interfaces.extras_interface import Extras
from DNA_analyser_IBP.interfaces.g4hunter_interface import G4Hunter
from DNA_analyser_IBP.interfaces.g4killer_interface import G4Killer
from DNA_analyser_IBP.interfaces.p53_interface import P53
from DNA_analyser_IBP.interfaces.rloopr_interface import Rloopr
from DNA_analyser_IBP.interfaces.zdna_interface import ZDna
from DNA_analyser_IBP.interfaces.cpg_interface import CpG
from DNA_analyser_IBP.interfaces.sequence_interface import Sequence

if TYPE_CHECKING:
    from DNA_analyser_IBP.ports import Ports

__all__ = ["Interfaces"]


class Interfaces:
    """
    Adapter class
    """

    def __init__(self, ports: "Ports"):
        """
        Create all interfaces
        """
        self.sequence: Sequence = Sequence(ports=ports)
        self.g4hunter: G4Hunter = G4Hunter(ports=ports)
        self.g4killer: G4Killer = G4Killer(ports=ports)
        self.p53_predictor: P53 = P53(ports=ports)
        self.rloopr: Rloopr = Rloopr(ports=ports)
        self.zdna: ZDna = ZDna(ports=ports)
        self.cpg: CpG = CpG(ports=ports)
        self.extras: Extras = Extras()
