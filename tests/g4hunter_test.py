import time

import pandas as pd
import pytest

from DNA_analyser_IBP.callers.sequence_caller import SequenceModel
from DNA_analyser_IBP.callers.user_caller import User
from DNA_analyser_IBP.callers.g4hunter_caller import (
    G4HunterAnalyse,
    G4HunterAnalyseFactory,
    g4_delete_analyse,
    g4_load_by_id,
    g4_load_all,
    g4_export_csv,
)

from . import vcr_instance


@pytest.fixture(scope="module")
@vcr_instance.use_cassette
def user():
    return User(
        email="user@mendelu.cz", password="user", server="http://localhost:8080/api"
    )


@pytest.fixture(scope="module")
def sequence():
    return SequenceModel(
        id="987acc67-5714-47b1-b56f-1dc56ded7c87",
        name="n",
        created="c",
        type="t",
        circular="cr",
        length=100,
        ncbi="NCB",
        tags=["ss"],
        fastaComment=None,
        nucleicCounts=None,
    )


@pytest.fixture(scope="module")
def g4_analyse():
    return G4HunterAnalyse(
        id="some_id",
        created="start_date",
        tags=["tag1", "tag2"],
        finished="end_date",
        title="some_title",
        sequenceId="some_sequence_id",
        resultCount=128,
        windowSize=20,
        threshold=1.5,
        frequency=1.2,
    )


@pytest.fixture(scope="module")
@vcr_instance.use_cassette
def load_first_g4(user):
    g4_lst = [g4 for g4 in g4_load_all(user, filter_tag=["demo"])]
    return g4_lst[0]


@vcr_instance.use_cassette
def test_g4hunter_creation_and_retrieving_data_frame(g4_analyse):
    """It should create g4hunter object + test pandas dataframe creation."""

    assert isinstance(g4_analyse, G4HunterAnalyse)  # object creation
    data_frame = g4_analyse.get_dataframe()  # testing dataframe creation
    assert isinstance(data_frame, pd.DataFrame)
    assert data_frame["id"][0] is "some_id"
    assert data_frame["sequence_id"][0] is "some_sequence_id"


@vcr_instance.use_cassette
def test_g4_hunter_creation_and_deleting(user, sequence):
    """It should create g4hunter analyse + then deletes it."""

    factory = G4HunterAnalyseFactory(
        user=user,
        id=sequence.id,
        tags=["test", "sequence"],
        threshold=0.8,
        window_size=20,
    )

    analyse = factory.analyse
    assert isinstance(analyse, G4HunterAnalyse)
    assert analyse.title == "Escherichia coli str. K-12 substr. MG1655"

    # time.sleep(2)

    res = g4_delete_analyse(user=user, id=analyse.id)
    assert res is True


@vcr_instance.use_cassette
def test_g4hunter_fail_delete(user, g4_analyse):
    """It should test deleting non existing analyse."""

    res = g4_delete_analyse(user, id=g4_analyse.id)
    assert res is False


@pytest.mark.parametrize(
    ["threshold", "window_size"], [(0, 10), (5, 10), (2, 200), (2, 2)]
)
@vcr_instance.use_cassette
def test_g4hunter_analyse_factory_for_wrong_values(
    user, sequence, threshold, window_size
):
    """It should throw exception for wrong values"""

    with pytest.raises(ValueError):
        _ = G4HunterAnalyseFactory(
            user=user,
            id=sequence.id,
            tags=["test", "sequence"],
            threshold=threshold,
            window_size=window_size,
        )


@vcr_instance.use_cassette
def test_load_all_g4hunters(user):
    """It should test retrieving list with all g4hunter analyses"""

    g4_lst = [g4 for g4 in g4_load_all(user, filter_tag=[])]
    assert len(g4_lst) == 2
    assert isinstance(g4_lst[0], G4HunterAnalyse)


@vcr_instance.use_cassette
def test_load_filtered_g4hunters(user):
    """It should test retrieving list with filtered g4hunter analyses"""

    g4_lst = [g4 for g4 in g4_load_all(user, filter_tag=["demo"])]
    assert len(g4_lst) == 2
    assert isinstance(g4_lst[0], G4HunterAnalyse)
    assert g4_lst[0].tags == "demo"


@vcr_instance.use_cassette
def test_load_g4hunter_by_id(user, load_first_g4):
    """It should return same g4hunter analyse with same id"""

    compare_g4 = g4_load_by_id(user, id=load_first_g4.id)
    assert isinstance(compare_g4, G4HunterAnalyse)
    assert load_first_g4.id == compare_g4.id


@vcr_instance.use_cassette
def test_exporting_g4analyse_to_csv(user, load_first_g4):
    """It should return string with csv for save to file"""

    data_aggregate = g4_export_csv(user, id=load_first_g4.id, aggregate=True)
    assert isinstance(data_aggregate, str)

    data_full = g4_export_csv(user, id=load_first_g4.id, aggregate=False)
    assert isinstance(data_full, str)
    assert len(data_aggregate) < len(data_full)


@vcr_instance.use_cassette
def test_g4hunter_analyse_factory_for_wrong_server(user, sequence):
    """It should test raising connection error for wrong server"""

    usr = user
    usr.server = "http://some_html_bullshit.cz"

    with pytest.raises(Exception):
        _ = G4HunterAnalyseFactory(
            user=usr,
            sequence_id=sequence.id,
            tags=["test", "sequence"],
            threshold=1.5,
            window_size=20,
        )
