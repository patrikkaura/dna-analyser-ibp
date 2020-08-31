# g4hunter.py

from DNA_analyser_IBP.models import Analyse


class G4Hunter(Analyse):
    """
    G4Hunter model object
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.result_count = kwargs.get("resultCount")
        self.threshold = kwargs.get("threshold")
        self.frequency = kwargs.get("frequency")
        self.window_size = kwargs.get("windowSize")

    def __str__(self):
        return f"G4HunterModel {self.id} {self.title}"

    def __repr__(self):
        return f"<G4HunterModel {self.id} {self.title}>"
