import time
import pytest
import pandas as pd

from . import DEV_URL
from DNA_analyser_IBP.callers import (
    FileSequenceFactory,
    NCBISequenceFactory,
    SequenceModel,
    TextSequenceFactory,
    seq_delete,
    seq_load_all,
    seq_load_by_id,
    seq_load_data,
    User
)


@pytest.fixture(scope="module")
def user():
    return User(email="user@mendelu.cz", password="user", server=DEV_URL)


@pytest.fixture(scope="module")
def host():
    return User(email="host", password="host", server=DEV_URL)


@pytest.fixture(scope="module")
def sequence():
    return SequenceModel(
        id="some_random_id",
        name="NC_006591.3 Canis lupus familiaris breed boxer chromosome 9",
        created="c",
        type="t",
        circular="cr",
        length=100,
        ncbi="NCB",
        tags=["ss"],
        fastaComment=None,
        nucleicCounts=None,
    )


class TestSequence:

    def test_sequence_creation_and_retrieving_data_frame(self, user):
        """It should create sequence object + test pandas dataframe creation."""

        sequence = SequenceModel(
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
        assert isinstance(sequence, SequenceModel)
        data_frame = sequence.get_dataframe()
        assert isinstance(data_frame, pd.DataFrame)
        assert data_frame["id"][0] is "987acc67-5714-47b1-b56f-1dc56ded7c87"
        assert data_frame["length"][0] == 100
        assert data_frame["fasta_comment"][0] is None

    def test_sequence_text_creation_and_deleting(self, host):
        """It should create sequence from RAW text + then deletes it."""

        factory = TextSequenceFactory(user=host,
                                      circular=True,
                                      data="ATTCGTTTAGGG",
                                      name="Test",
                                      tags=["testovaci", "test"],
                                      sequence_type="DNA")
        text_sequence = factory.sequence
        assert isinstance(text_sequence, SequenceModel)
        assert text_sequence.name == "Test"
        time.sleep(2)
        res = seq_delete(user=host, id=text_sequence.id)
        assert res is True

    def test_sequence_ncbi_creation_and_deleting(self, host):
        """It should create sequence from RAW text + then deletes it."""

        factory = NCBISequenceFactory(user=host,
                                      circular=True,
                                      name="Theobroma cacao chloroplast",
                                      tags=["Theobroma", "cacao"],
                                      ncbi_id="NC_014676.2")
        ncbi_sequence = factory.sequence
        assert isinstance(ncbi_sequence, SequenceModel)
        assert ncbi_sequence.name == "Theobroma cacao chloroplast"
        time.sleep(2)
        res = seq_delete(user=host, id=ncbi_sequence.id)
        assert res is True

    def test_sequence_file_uploading_creation_and_deleting(self, host):
        """It should create sequence from FASTA file + then deletes it."""

        factory = FileSequenceFactory(user=host,
                                      circular=True,
                                      file_path="/home/patrikkaura/Git/DNA_analyser_IBP/tests/sequence.txt",
                                      name="Saccharomyces cerevisiae",
                                      tags=["Saccharomyces"],
                                      sequence_type="DNA",
                                      format="FASTA")
        file_sequence = factory.sequence
        assert isinstance(file_sequence, SequenceModel)
        assert file_sequence.name == "Saccharomyces cerevisiae"
        time.sleep(2)
        res = seq_delete(user=host, id=file_sequence.id)
        assert res is True

    def test_sequence_fail_delete(self, host, sequence):
        """It should test deleting non existing sequence."""

        res = seq_delete(user=host, id=sequence.id)
        assert res is False

    def test_load_all_sequence_filtered(self, user):
        """It should test loading filtered list of all sequences."""

        sq_lst = [se for se in seq_load_all(user=user, filter_tag=[""])]
        assert len(sq_lst) == 1
        assert isinstance(sq_lst[0], SequenceModel)
        assert sq_lst[0].tags == "pes"

    def test_load_sequence_by_id(self, user):
        """It should return same object as first object in load all sequence."""

        sq_lst = [se for se in seq_load_all(user, filter_tag=["pes"])]
        test_sequence = sq_lst[0]
        compare_sequence = seq_load_by_id(user, id=test_sequence.id)
        assert isinstance(test_sequence, SequenceModel)
        assert test_sequence.id == compare_sequence.id

    def test_load_sequence_by_wrong_id(self, user):
        """It should return exception for loading sequence with shitty id."""

        with pytest.raises(Exception):
            seq_load_by_id(user, id="random_id")

    def test_loading_sequence_data(self, user):
        """It should return data of given sequence."""

        sq_lst = [se for se in seq_load_all(user=user, filter_tag=["pes"])]
        data = seq_load_data(user, id=sq_lst[0].id, data_len=100, pos=0)
        assert isinstance(data, str)
        assert len(data) == 100
        # time.sleep(1)

    @pytest.mark.parametrize(
        ["_len", "pos", "seq_len"],
        [(-10, 10, 100), (-20, -200, 100), (20, -211, 100), (10, 10, 19)],
    )
    def test_loading_sequence_data(self, user, _len, pos, seq_len):
        sq_lst = [se for se in seq_load_all(user, filter_tag=["pes"])]
        with pytest.raises(ValueError):
            _ = seq_load_data(user=user, id=sq_lst[0].id, data_len=_len, pos=pos, seq_len=seq_len)

    def test_load_all_sequence_not_filtered(self, user):
        """It should test loading list of all sequences."""

        sq_lst = [se for se in seq_load_all(user, filter_tag=[])]
        assert len(sq_lst) == 4
        assert isinstance(sq_lst[0], SequenceModel)

    def test_wrong_data_to_text_sequence_factory(self, user):
        """It should test raising type error for wrong data given into factory."""

        with pytest.raises(TypeError):
            _ = TextSequenceFactory(user=user,
                                    circularlll=True,
                                    data="ATTCGTTTAGGG",
                                    namelll="Test",
                                    tags=["testovaci", "test"],
                                    _type="DNA")

    def test_sequence_factory_for_wrong_server(user, sequence):
        """It should test raising connection error for wrong server"""
        usr = user
        usr.server = "http://some_html_bullshit.cz"

        with pytest.raises(Exception):
            _ = TextSequenceFactory(user=usr,
                                    circular=True,
                                    data="ATTCGTTTAGGG",
                                    name="Test",
                                    tags=["testovaci", "test"],
                                    _type="DNA")
