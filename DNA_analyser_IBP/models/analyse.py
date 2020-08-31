# analyse.py

from DNA_analyser_IBP.models.base import Base


class Analyse(Base):
    """
    Analyse model used in g4hunter
    """

    def __init__(self, **kwargs):
        super().__init__()

        self.id = kwargs.get("id")
        self.title = kwargs.get("title")
        self.tags = ", ".join(kwargs.get("tags"))
        self.created = kwargs.get("created")
        self.finished = kwargs.get("finished")
        self.sequence_id = kwargs.get("sequenceId")
