import pytest

from . import DEV_URL
from DNA_analyser_IBP.callers import P53Analyse, P53AnalyseFactory, User


@pytest.fixture(scope="module")
def user():
    return User(email="host", password="host", server=DEV_URL)


class TestP53:

    def test_p53_creation(self, user):
        """It should create p53 object"""

        sequence = "GGACATGCCCGGGCATGTCC"
        p53 = P53AnalyseFactory(user=user, sequence=sequence).analyse
        assert isinstance(p53, P53Analyse)
        assert sequence == p53.sequence
        assert len(sequence) == p53.length
        assert p53.difference == -7.61
        assert p53.affinity == 1

    @pytest.mark.parametrize(
        ["sequence", "e"],
        [("AATTATA", ValueError),
         ("", ValueError),
         ("AATATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", ValueError),
         ("        ", ValueError)],
    )
    def test_p53_exception(self, user, sequence, e):
        """It should raise exception for wrong sequence len"""

        with pytest.raises(e):
            _ = P53AnalyseFactory(user=user, sequence=sequence)
