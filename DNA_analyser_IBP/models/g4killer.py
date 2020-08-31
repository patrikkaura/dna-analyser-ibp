# g4killer.py

from DNA_analyser_IBP.models.base import Base


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
        self.mutation_sequences = kwargs.get("mutationSequences")

    def __str__(self):
        return f"G4Killer {self.origin_sequence} {self.mutation_sequences[0]}"

    def __repr__(self):
        return f"<G4Killer {self.origin_sequence} {self.mutation_sequences[0]}>"
