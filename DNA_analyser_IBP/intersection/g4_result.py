# g4hunter.py

import csv
from typing import List

from DNA_analyser_IBP.utils import exception_handler


class G4Result:
    """G4Hunter result object"""

    def __init__(self, position: int, length: int, score: float):
        self.score = score
        self.length = length
        self.position = position
        self.middle = self.position + (self.length // 2)

    def get_group_id(self) -> int:
        """
        Get group id used in annotation intersection

        Returns:
            (int): group id
        """
        if self.score <= 1.2:
            return 1
        elif 1.2 < self.score <= 1.4:
            return 4
        elif 1.4 < self.score <= 1.6:
            return 7
        elif 1.6 < self.score <= 1.8:
            return 10
        elif 1.8 < self.score <= 2.0:
            return 13
        elif 2.0 < self.score:
            return 16


@exception_handler
def create_g4hunter_list(analyse: str) -> List[G4Result]:
    """
    Return list of G4Result objects

    Returns:
        (List[G4Result]): G4Hunter results
    """
    analyse_list: list = list()
    with open(analyse, "r") as file:
        reader = csv.reader(file, delimiter="\t")
        next(reader)
        for row in reader:
            analyse_list.append(
                G4Result(position=int(row[1]), length=int(row[2]), score=float(row[4]))
            )
        return analyse_list
