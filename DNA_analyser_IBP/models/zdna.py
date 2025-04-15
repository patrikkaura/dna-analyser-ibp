# zdna.py

from DNA_analyser_IBP.models import Analyse


class ZDna(Analyse):
    """
    Z-DNA hunter model object
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.result_count = kwargs.get("resultCount")
        self.model = kwargs.get("selectedModel")
        self.min_sequence_size=kwargs.get("minSequenceSize")
        self.GC_score = kwargs.get("score_gc")
        self.GTAC_score = kwargs.get("score_gtac")
        self.AT_score = kwargs.get("score_at")
        self.oth_score = kwargs.get("score_oth")
        self.min_score_percentage = kwargs.get("threshold")

    def __str__(self):
        return f"Z-DnaHunterModel {self.id} {self.title}"

    def __repr__(self):
        return f"<Z-DnaHunterModel {self.id} {self.title}>"