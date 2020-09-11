import pytest

from typing import List

from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.models import User, Sequence
from DNA_analyser_IBP.adapters import Adapters, UserAdapter


@pytest.fixture(scope="module")
def adapters():
    user: User = UserAdapter.sign_in(
        User(email="host", password="host", server=Config.SERVER_CONFIG.PRODUCTION)
    )
    adapters = Adapters(user=user)
    return adapters


class TestSequenceAdapter:

    def test_load_all_sequences(self, adapters: Adapters) -> None:
        """It should return iterator with Sequence models"""
        sequence_generator = adapters.sequence.load_all(tags=list())

        sequence_list = [sequence for sequence in sequence_generator]
        assert len(sequence_list) == 5

        for sequence in sequence_list:
            assert isinstance(sequence, Sequence)

    def test_load_by_id_sequence(self, adapters: Adapters) -> None:
        """It should return Sequence models"""
        sequence_generator = adapters.sequence.load_all(tags=list())
        sequence_list: List[Sequence] = [sequence for sequence in sequence_generator]

        sequence_id = sequence_list[0].id
        sequence = adapters.sequence.load_by_id(id=sequence_id)
        assert isinstance(sequence, Sequence)

    def test_load_sequence_data(self, adapters: Adapters) -> None:
        """It should return string with sequence data"""
        sequence_generator = adapters.sequence.load_all(tags=list())
        sequence_list: List[Sequence] = [sequence for sequence in sequence_generator]

        sequence = sequence_list[-1]
        sequence_data = adapters.sequence.load_data(id=sequence.id, length=20, position=10, sequence_length=sequence.length)
        assert isinstance(sequence_data, str)
        assert len(sequence_data) == 20

    def test_load_sequence_data_with_wrong_params(self, adapters: Adapters) -> None:
        """It should return string with sequence data"""
        sequence_generator = adapters.sequence.load_all(tags=list())
        sequence_list: List[Sequence] = [sequence for sequence in sequence_generator]

        sequence = sequence_list[0]
        sequence_data = adapters.sequence.load_data(id=sequence.id, length=90000, position=-1, sequence_length=sequence.length)
        assert sequence_data is None

    def test_delete_sequence(self, adapters: Adapters) -> None:
        """It should delete sequence one from server"""

        sequence_generator = adapters.sequence.load_all(tags=list())
        sequence_list: List[Sequence] = [sequence for sequence in sequence_generator]

        for sequence in sequence_list:
            deleted = adapters.sequence.delete(id=sequence.id)
            assert deleted is True

    def test_text_sequence_creation(self, adapters: Adapters) -> None:
        """It should create sequence from text and return object"""

        sequence: Sequence = adapters.sequence.create_text_sequence(
            circular=True, data='ATATATATAT', name='test_text_sequence', tags=['test'], nucleic_type='DNA'
        )
        assert isinstance(sequence, Sequence)

    @pytest.mark.skip(reason='in pipeline cannot provide file path')
    def test_fasta_sequence_creation(self, adapters: Adapters) -> None:
        """It should create sequence from file and return object"""

        sequence: Sequence = adapters.sequence.create_file_sequence(
            circular=True,
            path='./sequence_samples/fasta_sample.txt',
            name='test_file_sequence',
            tags=['test'],
            nucleic_type='DNA',
            format='FASTA',
        )
        assert isinstance(sequence, Sequence)

    def test_ncbi_sequence_creation(self, adapters: Adapters) -> None:
        """It should create sequence from NCBI and return object"""

        sequence: Sequence = adapters.sequence.create_ncbi_sequence(
            circular=False, name="test_ncbi_sequence", tags=['test'], ncbi_id='NC_014676.2'
        )
        assert isinstance(sequence, Sequence)
