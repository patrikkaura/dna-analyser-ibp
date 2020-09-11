import pytest

from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.models import User, G4Killer
from DNA_analyser_IBP.adapters import Adapters, UserAdapter

ORIGIN_SEQUENCE = "AGGAGGGTAAGGGTGAGTTGGGTAATTGGGGGGCATGGTTAGG"


@pytest.fixture(scope="module")
def adapters():
    user: User = UserAdapter.sign_in(
        User(email="host", password="host", server=Config.SERVER_CONFIG.PRODUCTION)
    )
    adapters = Adapters(user=user)
    return adapters


class TestG4KillerAdapter:
    def test_g4killer_creation(self, adapters: Adapters) -> None:
        """It should create G4Killer model and return result data"""

        g4killer = adapters.g4killer.create_analyse(
            sequence=ORIGIN_SEQUENCE, threshold=1.0, complementary=False
        )

        # assert instance
        assert isinstance(g4killer, G4Killer)

        # assert values
        assert g4killer.origin_sequence == ORIGIN_SEQUENCE
        assert not g4killer.on_complementary
        assert g4killer.target_threshold == 1.0
        assert g4killer.mutation_score <= 1.0

    @pytest.mark.parametrize(
        "threshold,expected",
        [(-1, None), (20, None), (-0.00001, None), (4.0001, None)],
    )
    def test_g4killer_creation_fail(
        self, adapters: Adapters, threshold: float, expected: None
    ) -> None:
        """It should create G4Killer model and return result data"""

        g4killer = adapters.g4killer.create_analyse(
            sequence=ORIGIN_SEQUENCE, threshold=threshold, complementary=False
        )

        # assert instance
        assert g4killer is expected
