import pytest

from . import DEV_URL
from DNA_analyser_IBP.callers import (
    G4KillerAnalyse,
    G4KillerAnalyseFactory,
    User
)


@pytest.fixture(scope="module")
def user():
    return User(email="test@python.cz", password="test", server=DEV_URL)


@pytest.fixture(scope="module")
def origin():
    return "AGGAGGGTAAGGGTGAGTTGGGTAATTGGGGGGCATGGTTAGG"


class TestG4Killer:

    def test_g4killer_creation(self, user, origin):
        """It should create g4killer object and lower gscore"""

        gkill = G4KillerAnalyseFactory(user=user, sequence=origin, threshold=1.0, complementary=False).analyse
        assert isinstance(gkill, G4KillerAnalyse)
        assert origin == gkill.origin_sequence
        assert gkill.origin_sequence != gkill.mutation_sequences[0]
        assert gkill.mutation_score < gkill.origin_score
