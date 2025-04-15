# __init__.py

from typing import TYPE_CHECKING

from DNA_analyser_IBP.ports.batch_port import BatchPort
from DNA_analyser_IBP.ports.g4hunter_port import G4HunterPort
from DNA_analyser_IBP.ports.g4killer_port import G4KillerPort
from DNA_analyser_IBP.ports.p53_port import P53Port
from DNA_analyser_IBP.ports.rloopr_port import RlooprPort
from DNA_analyser_IBP.ports.zdna_port import ZDnaPort
from DNA_analyser_IBP.ports.cpg_port import CpGPort
from DNA_analyser_IBP.ports.sequence_port import SequencePort

if TYPE_CHECKING:
    from DNA_analyser_IBP.models import User

__all__ = ["Ports"]


class Ports:
    """
    Ports class
    """

    def __init__(self, user: "User"):
        self.p53: P53Port = P53Port(user=user)
        self.batch: BatchPort = BatchPort(user=user)
        self.g4killer: G4KillerPort = G4KillerPort(user=user)
        self.g4hunter: G4HunterPort = G4HunterPort(user=user)
        self.sequence: SequencePort = SequencePort(user=user)
        self.rloopr: RlooprPort = RlooprPort(user=user)
        self.zdna: ZDnaPort = ZDnaPort(user=user)
        self.cpg: CpGPort = CpGPort(user=user)
