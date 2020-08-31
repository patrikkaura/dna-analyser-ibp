# p53.py

from DNA_analyser_IBP.models.base import Base


class P53(Base):
    """
    P53 model object
    """

    def __init__(self, **kwargs):
        super().__init__()

        self.sequence = kwargs.get("sequence")
        self.affinity = kwargs.get("affinity")
        self.predictor = kwargs.get("predictor")
        self.difference = kwargs.get("difference")
        self.length = kwargs.get("length")
        self.position = kwargs.get("position")

    def __str__(self):
        return f"P53Model {self.sequence}"

    def __repr__(self):
        return f"<P53Model {self.sequence}>"
