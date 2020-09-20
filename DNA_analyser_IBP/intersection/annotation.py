# annotation.py

import csv
from typing import List

from DNA_analyser_IBP.intersection.g4_result import G4Result
from DNA_analyser_IBP.utils import exception_handler


class Annotation:
    """Annotations object used for intersections"""

    def __init__(self, start: int, end: int, feature: str, area: int):
        self.start = start
        self.end = end
        self.after = self.end + area
        self.before = self.start - area if self.start > area else 0
        self.feature = feature

    def is_in(self, analyse: G4Result) -> bool:
        """
        Test if PQS in <start, end> anotation

        Args:
            analyse (G4Result): G4hunter analyse result

        Returns:
            (bool): True = inside, False = not
        """
        return self.start <= analyse.middle <= self.end

    def is_before(self, analyse: G4Result) -> bool:
        """
        Test if PQS in before <-100, start) anotation

        Args:
            analyse (G4Result): G4hunter analyse result

        Returns:
            (bool): True = before, False = not
        """
        return self.before <= analyse.middle < self.start

    def is_after(self, analyse: G4Result) -> bool:
        """
        Test if PQS in after (end, +100> anotation

        Args:
            analyse (G4Result): G4hunter analyse result

        Returns:
            (bool): True = after, False = not
        """
        return self.end < analyse.middle <= self.after


@exception_handler
def create_annotation_list(annotation: str, area_size: int) -> List[Annotation]:
    """
    Return list of Annotation objects

    Args:
        annotation (str): path to parsed annotation file
        area_size (int): size of overlay region outside annotation [Default=100]

    Returns:
        (List[annotation]): annotations
    """
    annotation_list: list = list()

    with open(annotation, "r") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)
        for row in reader:
            annotation_list.append(
                Annotation(
                    start=int(row[1]),
                    end=int(row[2]),
                    feature=row[4],
                    area=area_size,
                )
            )
    annotation_list = sorted(annotation_list, key=lambda a: a.start)
    return annotation_list


@exception_handler
def get_annotation_labels(*, annotation_list: List[Annotation]) -> List[str]:
    """Return list with all annotation labels

    Args:
        annotation_list (List[Annotation]): parsed files of annotations

    Returns:
        List[str]: list of all annotation labels e.g. ['CDS', 'rRNA', ...]
    """
    label_list: list = list()
    for annotation in annotation_list:
        if annotation.feature not in label_list:
            label_list.append(annotation.feature)
    return label_list
