# batch.py

from DNA_analyser_IBP.batch_statuses import BatchStatus
from DNA_analyser_IBP.models.base import Base


class Batch(Base):
    """
    Batch model object
    """

    def __init__(self, **kwargs):
        self.cpu_time = kwargs.get("cpuTime")
        self.created = kwargs.get("created")
        self.exception = kwargs.get("exception")
        self.finished = kwargs.get("finished")
        self.name = kwargs.get("name")
        self.progress = kwargs.get("progress")
        self.started = kwargs.get("started")
        self.status = kwargs.get("status")

    def __str__(self):
        return f"Batch {self.name}"

    def __repr__(self):
        return f"<Batch {self.name}>"

    def is_finished(self) -> bool:
        """
        Return if batch is finished
        """
        return self.status == BatchStatus.FINISH

    def is_failed(self) -> bool:
        """
        Return if batch is failed
        """
        return self.status == BatchStatus.FAILED
