# sequence.py


from DNA_analyser_IBP.models.base import Base


class Sequence(Base):
    """
    Sequence model object
    """

    def __init__(self, **kwargs):
        super().__init__()

        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.type = kwargs.get("type")
        self.tags = ", ".join(kwargs.get("tags"))
        self.length = kwargs.get("length")
        self.circular = kwargs.get("circular")
        self.created = kwargs.get("created")
        self.ncbi = kwargs.get("ncbi")
        self.fasta_comment = kwargs.get("fastaComment")
        self.gc_count = None
        self.nucleic_count = None
        self.__get_gc_count(kwargs.get("nucleicCounts"))

    def __str__(self):
        return f"SequenceModel {self.id} {self.name} {self.type}"

    def __repr__(self):
        return f"<SequenceModel {self.id} {self.name} {self.type}>"

    def __get_gc_count(self, nucleic_dict: dict) -> None:
        """
        Get GC count from nucleic count dict

        Args:
            nucleic_dict (dict): structure with Guanine and Cytosine counts
        """
        if nucleic_dict is not None:
            self.nucleic_count = str(nucleic_dict)
            self.gc_count = int(nucleic_dict.get("C", 0)) + int(
                nucleic_dict.get("G", 0)
            )
