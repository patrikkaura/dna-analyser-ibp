import pytest

import time
import pandas as pd
from . import DEV_URL

from DNA_analyser_IBP.callers import (
    SequenceModel,
    SequenceMethods,
    TextSequenceFactory,
    User,
    G4HunterAnalyse,
    G4HunterAnalyseFactory,
    G4HunterMethods,
)


@pytest.fixture(scope="module")
def user():
    return User(email="test@python.cz", password="test", server=DEV_URL)


@pytest.fixture(scope="module")
def sequence():
    return SequenceModel(id="987acc67-5714-47b1-b56f-1dc56ded7c87",
                         name="n",
                         created="c",
                         type="t",
                         circular="cr",
                         length=100,
                         ncbi="NCB",
                         tags=["ss"],
                         fastaComment=None,
                         nucleicCounts=None)


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
def load_first_g4(user):
    g4_lst = [g4 for g4 in G4HunterMethods.load_all(user, tags=[])]
    return g4_lst[0]


class TestG4Hunter:

    def test_g4hunter_creation_and_retrieving_data_frame(self, g4_analyse):
        """It should create g4hunter object + test pandas dataframe creation."""

        assert isinstance(g4_analyse, G4HunterAnalyse)  # object creation
        data_frame = g4_analyse.get_dataframe()  # testing dataframe creation
        assert isinstance(data_frame, pd.DataFrame)
        assert data_frame["id"][0] is "some_id"
        assert data_frame["sequence_id"][0] is "some_sequence_id"

    def test_g4_hunter_creation_and_deleting(self, user):
        """It should create g4hunter analyse + then deletes it."""

        test = TextSequenceFactory(user=user,
                                   circular=True,
                                   data="ATTCGTTTAGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGggG",
                                   name="Test",
                                   tags=["testovaci", "test"],
                                   nucleic_type="DNA").sequence

        factory = G4HunterAnalyseFactory(
            user=user,
            id=test.id,
            tags=["test", "sequence"],
            threshold=0.8,
            window_size=20,
        )
        analyse = factory.analyse
        assert isinstance(analyse, G4HunterAnalyse)
        assert analyse.title == "Test"
        time.sleep(2)
        res = G4HunterMethods.delete(user=user, id=analyse.id)
        assert res
        res = SequenceMethods.delete(user=user, id=test.id)
        assert res

    def test_g4hunter_fail_delete(self, user, g4_analyse):
        """It should test deleting non existing analyse."""
        res = G4HunterMethods.delete(user, id=g4_analyse.id)
        assert res is False

    def test_load_all_g4hunters(self, user):
        """It should test retrieving list with all g4hunter analyses"""

        g4_lst = [g4 for g4 in G4HunterMethods.load_all(user, tags=[])]
        assert isinstance(g4_lst[0], G4HunterAnalyse)

    def test_load_g4hunter_by_id(self, user, load_first_g4):
        """It should return same g4hunter analyse with same id"""

        compare_g4 = G4HunterMethods.load_by_id(user, id=load_first_g4.id)
        assert isinstance(compare_g4, G4HunterAnalyse)
        assert load_first_g4.id == compare_g4.id

    def test_exporting_g4analyse_to_csv(self, user, load_first_g4):
        """It should return string with csv for save to file"""

        data_aggregate = G4HunterMethods.export_csv(user, id=load_first_g4.id, aggregate=True)
        assert isinstance(data_aggregate, str)
        data_full = G4HunterMethods.export_csv(user, id=load_first_g4.id, aggregate=False)
        assert isinstance(data_full, str)
        assert len(data_aggregate) < len(data_full)

    def test_g4hunter_analyse_factory_for_wrong_server(self, user, sequence):
        """It should test raising connection error for wrong server"""

        usr = user
        usr.server = "http://some_html_bullshit.cz"

        with pytest.raises(Exception):
            _ = G4HunterAnalyseFactory(user=usr,
                                       sequence_id=sequence.id,
                                       tags=["test", "sequence"],
                                       threshold=1.5,
                                       window_size=20)
