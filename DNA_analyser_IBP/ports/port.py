# port.py

from typing import TYPE_CHECKING

from DNA_analyser_IBP.adapters import Adapters
from DNA_analyser_IBP.models import User

if TYPE_CHECKING:
    from DNA_analyser_IBP.models import User


class Port:
    """
    Base port class
    """

    def __init__(self, user: "User"):
        self.user: "User" = user
        self.adapter: "Adapters" = Adapters(user=user)
