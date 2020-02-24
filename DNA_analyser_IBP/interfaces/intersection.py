# intersection.py
# !/usr/bin/env python3


class G4Result:
    """G4Hunter result object"""

    def __init__(self, position: int, length: int, score: float):
        self.position = position
        self.length = length
        self.score = score

    def get_group_id(self) -> int:
        """
        Get group id used in anotation intersection

        Returns:
            (int): group id
        """
        if self.score <= 1.2:
            return 1
        elif 1.2 < self.score <= 1.4:
            return 2
        elif 1.4 < self.score <= 1.6:
            return 3
        elif 1.6 < self.score <= 1.8:
            return 4
        elif 1.8 < self.score <= 2.0:
            return 5
        elif 2.0 < self.score:
            return 6


class Anotation:
    """Anotations object used for intersections"""

    def __init__(self, start: int, end: int, feature: str):
        self.start = start
        self.before = self.start - 100 if self.start > 100 else 0
        self.end = end
        self.after = self.end + 100
        self.feature = feature

    def is_in(self, analyse: G4Result) -> bool:
        """
        Test if PQS in <start, end> anotation

        Args:
            analyse (G4Result): G4hunter analyse result

        Returns:
            (bool): True = inside, False = not
        """
        return self.start <= analyse.position <= self.end

    def is_before(self, analyse: G4Result) -> bool:
        """
        Test if PQS in before <-100, start) anotation

        Args:
            analyse (G4Result): G4hunter analyse result

        Returns:
            (bool): True = before, False = not
        """
        return self.before <= analyse.position < self.start

    def is_after(self, analyse: G4Result) -> bool:
        """
        Test if PQS in after (end, +100> anotation

        Args:
            analyse (G4Result): G4hunter analyse result

        Returns:
            (bool): True = after, False = not
        """
        return self.end < analyse.position <= self.after
