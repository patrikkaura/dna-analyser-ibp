import pytest

from typing import List

from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.models import User, G4Hunter, Sequence
from DNA_analyser_IBP.adapters import Adapters, UserAdapter


@pytest.fixture(scope="module")
def adapters():
    user: User = UserAdapter.sign_in(
        User(email="host", password="host", server=Config.SERVER_CONFIG.PRODUCTION)
    )
    adapters = Adapters(user=user)
    return adapters


@pytest.fixture(scope="module")
def sequence(adapters):
    sequence_generator = adapters.sequence.load_all(tags=list())
    sequence_list: List[Sequence] = [sequence for sequence in sequence_generator]
    return sequence_list[0]


class TestG4HunterAdapter:
    def test_g4hunter_analysis(self, adapters: Adapters, sequence: Sequence) -> None:
        """It should run g4hunter analysis and return G4Hunter object"""
        g4hunter: G4Hunter = adapters.g4hunter.create_analyse(
            id=sequence.id, tags=["test"], threshold=1.2, window_size=25,
        )
        assert isinstance(g4hunter, G4Hunter)

    def test_load_all_g4hunter(self, adapters: Adapters) -> None:
        """It should return iterator with G4Hunter models"""
        g4hunter_generator = adapters.g4hunter.load_all(tags=list())

        g4hunter_list = [g4hunter for g4hunter in g4hunter_generator]
        assert len(g4hunter_list) == 1

        for g4hunter in g4hunter_list:
            assert isinstance(g4hunter, G4Hunter)

    def test_load_by_id_g4hunter(self, adapters: Adapters) -> None:
        """It should return iterator with G4Hunter models"""
        g4hunter_generator = adapters.g4hunter.load_all(tags=list())
        g4hunter_list = [g4hunter for g4hunter in g4hunter_generator]

        g4hunter = adapters.g4hunter.load_by_id(id=g4hunter_list[0].id)
        assert isinstance(g4hunter, G4Hunter)

    def test_g4hunter_delete(self, adapters: Adapters) -> None:
        """It should delete g4hunter analysis"""
        g4hunter_generator = adapters.g4hunter.load_all(tags=list())
        g4hunter_list = [g4hunter for g4hunter in g4hunter_generator]

        assert len(g4hunter_list) == 1

        deleted: bool = adapters.g4hunter.delete(id=g4hunter_list[0].id)
        assert deleted is True
