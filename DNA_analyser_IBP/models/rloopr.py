# rloop.py

from DNA_analyser_IBP.models import Analyse


class RLoopr(Analyse):
    """
    Rloopr model object
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.model = kwargs.get("model")
        self.result_count = kwargs.get("resultCount")

    def __str__(self):
        return f"RLooprModel {self.id} {self.title}"

    def __repr__(self):
        return f"<RlooprModel {self.id} {self.title}>"
