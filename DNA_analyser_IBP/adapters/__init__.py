# __init__.py

from typing import TYPE_CHECKING

from DNA_analyser_IBP.adapters.batch_adapter import BatchAdapter
from DNA_analyser_IBP.adapters.g4hunter_adapter import G4HunterAdapter
from DNA_analyser_IBP.adapters.g4killer_adapter import G4KillerAdapter
from DNA_analyser_IBP.adapters.p53_adapter import P53Adapter
from DNA_analyser_IBP.adapters.rloopr_adapter import RLooprAdapter
from DNA_analyser_IBP.adapters.sequence_adapter import SequenceAdapter
from DNA_analyser_IBP.adapters.user_adapter import UserAdapter

if TYPE_CHECKING:
    from DNA_analyser_IBP.models import User

__all__ = ["Adapters", "UserAdapter"]


class Adapters:
    """
    Adapter class
    """

    def __init__(self, user: "User"):
        """
        Create all adapters
        """
        self.p53: P53Adapter = P53Adapter(user=user)
        self.batch: BatchAdapter = BatchAdapter(user=user)
        self.g4killer: G4KillerAdapter = G4KillerAdapter(user=user)
        self.sequence: SequenceAdapter = SequenceAdapter(user=user)
        self.g4hunter: G4HunterAdapter = G4HunterAdapter(user=user)
        self.rloopr: RLooprAdapter = RLooprAdapter(user=user)
