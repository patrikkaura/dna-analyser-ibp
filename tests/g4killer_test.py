import pytest
from . import DEV_URL
from DNA_analyser_IBP.callers import (
    G4KillerAnalyse,
    G4KillerAnalyseFactory,
    User
)


@pytest.fixture(scope="module")
def user():
    return User(email="host", password="host", server=DEV_URL)


@pytest.fixture(scope="module")
def origin():
    return "AGGAGGGTAAGGGTGAGTTGGGTAATTGGGGGGCATGGTTAGG"


class TestG4Killer:

    def test_g4killer_creation(self, user, origin):
        """It should create g4killer object and lower gscore"""

        gkill = G4KillerAnalyseFactory(user=user, origin_sequence=origin, threshold=1.0, on_complementary=False).analyse
        assert isinstance(gkill, G4KillerAnalyse)
        assert origin == gkill.origin_sequence
        assert gkill.origin_sequence != gkill.mutation_sequences[0]
        assert gkill.mutation_score < gkill.origin_score

    @pytest.mark.parametrize(["threshold", "e"],
                             [(-99.0, ValueError), (-0.00001, ValueError), (10000.0, ValueError)])
    def test_g4killer_exception(self, user, origin, threshold, e):
        """It should raise exception for wrong values"""

        with pytest.raises(e):
            _ = G4KillerAnalyseFactory(user=user, origin_sequence=origin, threshold=threshold, on_complementary=False)
