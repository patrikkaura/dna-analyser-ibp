import pytest

from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.models import User, P53
from DNA_analyser_IBP.adapters import Adapters, UserAdapter

SEQUENCE_WITH_CORRECT_LEGTH = "ACGACGACGCGCGACGACGC"
SEQUENCE_WITH_INCORRECT_LEGTH = "ATCG"


@pytest.fixture(scope="module")
def adapters():
    user: User = UserAdapter.sign_in(
        User(email="host", password="host", server=Config.SERVER_CONFIG.PRODUCTION)
    )
    adapters = Adapters(user=user)
    return adapters


class TestP53Adapter:
    def test_p53_creation(self, adapters: Adapters) -> None:
        """It should create P53 model and return result data"""

        p53 = adapters.p53.create_analyse(sequence=SEQUENCE_WITH_CORRECT_LEGTH)

        # assert instance
        assert isinstance(p53, P53)

        # assert values
        assert p53.sequence == SEQUENCE_WITH_CORRECT_LEGTH
        assert p53.length <= len(SEQUENCE_WITH_CORRECT_LEGTH)
        assert p53.affinity == 0.0

    def test_p53_creation_fail(self, adapters: Adapters) -> None:
        """It should not create P53 model"""

        p53 = adapters.p53.create_analyse(sequence=SEQUENCE_WITH_INCORRECT_LEGTH)

        # assert instance
        assert p53 is None
