# cpx.py

from DNA_analyser_IBP.models import Analyse


class CpG(Analyse):
    """
    CpG Hunter model object
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.result_count = kwargs.get("resultCount")
        self.min_window_size = kwargs.get("minWindowSize")
        self.min_gc_percentage = kwargs.get("minGcPercentage")
        self.min_obs_exp_cpg = kwargs.get("minObservedToExpectedCpG")
        self.min_island_merge_gap = kwargs.get("minIslandMergeGap")
        self.second_nucleotide = kwargs.get("secondNucleotide")

    def __str__(self):
        return f"CpXHunterModel {self.id} {self.title}"

    def __repr__(self):
        return f"<CpXHunterModel {self.id} {self.title}>"