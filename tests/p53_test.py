import pytest

from DNA_analyser_IBP.callers.user_caller import User
from DNA_analyser_IBP.callers.p53_caller import P53Analyse, P53AnalyseFactory

from . import vcr_instance


@pytest.fixture(scope="module")
@vcr_instance.use_cassette
def user():
    return User(
        email="user@mendelu.cz", password="user", server="http://localhost:8080/api"
    )


@vcr_instance.use_cassette
def test_p53_creation(user):
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
    [
        ("AATTATA", ValueError),
        ("", ValueError),
        ("AATATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", ValueError),
        ("        ", ValueError),
    ],
)
@vcr_instance.use_cassette
def test_p53_exception(user, sequence, e):
    """It should raise exception for wrong sequence len"""

    with pytest.raises(e):
        _ = P53AnalyseFactory(user=user, sequence=sequence)
