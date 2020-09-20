# batch_statuses.py


from typing import List


class BatchStatus:
    """
    Batch statuses constants
    """

    CREATED: str = "CREATED"
    WAITING: str = "WAITING"
    RUNNING: str = "RUNNING"
    FINISH: str = "FINISH"
    FAILED: str = "FAILED"

    @classmethod
    def all_batch_statuses(cls) -> List[str]:
        """
        Return all batch statuses
        """
        return [cls.CREATED, cls.WAITING, cls.RUNNING, cls.FINISH, cls.FAILED]
