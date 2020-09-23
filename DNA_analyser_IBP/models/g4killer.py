# g4killer.py

from DNA_analyser_IBP.models.base import Base

from typing import List


class G4Killer(Base):
    """
    G4Killer model object
    """

    def __init__(self, **kwargs):
        super().__init__()

        self.origin_score = kwargs.get("originScore")
        self.change_count = kwargs.get("changeCount")
        self.mutation_score = kwargs.get("mutationScore")
        self.origin_sequence = kwargs.get("originSequence")
        self.on_complementary = kwargs.get("onComplementary")
        self.target_threshold = kwargs.get("targetThreshold")
        self.mutation_variants = kwargs.get("mutationVariants")
        self.mutation_sequences = None
        self.mutation_sequences_transform(kwargs.get("mutationSequences"))

    def __str__(self):
        return f"G4Killer {self.origin_sequence}"

    def __repr__(self):
        return f"<G4Killer {self.origin_sequence}>"

    def mutation_sequences_transform(self, mutation_sequences: List[str]) -> None:
        """
        Transform server parameter mutationSequences into string

        Args:
            mutation_sequences (List[str]): original mutation list
        """
        if mutation_sequences:
            self.mutation_sequences = ", ".join(mutation_sequences)
