import pytest

from DNA_analyser_IBP.callers.g4killer_caller import (
    G4KillerAnalyse,
    G4KillerAnalyseFactory,
)
from DNA_analyser_IBP.callers.user_caller import User

from . import vcr_instance


@pytest.fixture(scope="module")
@vcr_instance.use_cassette
def user():
    return User(
        email="user@mendelu.cz", password="user", server="http://localhost:8080/api"
    )


@pytest.fixture(scope="module")
@vcr_instance.use_cassette
def origin():
    return "AGGAGGGTAAGGGTGAGTTGGGTAATTGGGGGGCATGGTTAGG"


@vcr_instance.use_cassette
def test_g4killer_creation(user, origin):
    """It should create g4killer object and lower gscore"""

    gkill = G4KillerAnalyseFactory(
        user=user, origin_sequence=origin, threshold=1.0
    ).analyse

    assert isinstance(gkill, G4KillerAnalyse)
    assert origin == gkill.origin_sequence
    assert gkill.origin_sequence != gkill.mutation_sequence
    assert gkill.mutation_score < gkill.origin_score


@pytest.mark.parametrize(
    ["threshold", "e"],
    [(-99.0, ValueError), (-0.00001, ValueError), (10000.0, ValueError)],
)
@vcr_instance.use_cassette
def test_g4killer_exception(user, origin, threshold, e):
    """It should raise exception for wrong values"""

    with pytest.raises(e):
        _ = G4KillerAnalyseFactory(
            user=user, origin_sequence=origin, threshold=threshold
        )
