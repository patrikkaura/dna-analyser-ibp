# type.py


from typing import List


class Types:
    """
    Object types
    """

    G4HUNTER: str = "G4HUNTER"
    PALINDROME: str = "PALINDROME"
    RLOOPR: str = "RLOOPR"
    SEQUENCE: str = "SEQUENCE"
    ZDNA: str = "ZDNA"
    CPG: str = "CPG"

    @classmethod
    def all_types(cls) -> List[str]:
        """
        Return all types
        """
        return [cls.G4HUNTER, cls.PALINDROME, cls.RLOOPR, cls.SEQUENCE, cls.ZDNA, cls.CPG]
