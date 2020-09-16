import pytest

from typing import List

from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.models import User, RLoopr, Sequence
from DNA_analyser_IBP.adapters import Adapters, UserAdapter


@pytest.fixture(scope="module")
def adapters():
    # TODO: change to PRODUCTION server when deployed
    user: User = UserAdapter.sign_in(
        User(email="host", password="host", server=Config.SERVER_CONFIG.LOCALHOST)
    )
    adapters = Adapters(user=user)
    return adapters


@pytest.fixture(scope="module")
def sequence(adapters):
    sequence_generator = adapters.sequence.load_all(tags=list())
    sequence_list: List[Sequence] = [sequence for sequence in sequence_generator]
    return sequence_list[0]


class TestRlooprAdapter:
    @pytest.mark.skip(reason="Not implemented in production environment!")
    def test_rloopr_analysis(self, adapters: Adapters, sequence: Sequence) -> None:
        """It should run rloopr analysis and return RLoopr object"""
        rloopr: RLoopr = adapters.rloopr.create_analyse(
            id=sequence.id, tags=["test"], riz_model=[0, 1],
        )
        assert isinstance(rloopr, RLoopr)

    @pytest.mark.skip(reason="Not implemented in production environment!")
    def test_load_all_rloopr(self, adapters: Adapters) -> None:
        """It should return iterator with RLoopr models"""
        rloopr_generator = adapters.rloopr.load_all(tags=list())

        rloopr_list = [rloopr for rloopr in rloopr_generator]
        assert len(rloopr_list) == 1

        for rloopr in rloopr_list:
            assert isinstance(rloopr, RLoopr)

    @pytest.mark.skip(reason="Not implemented in production environment!")
    def test_load_by_id_rloopr(self, adapters: Adapters) -> None:
        """It should return iterator with RLoopr models"""
        rloopr_generator = adapters.rloopr.load_all(tags=list())
        rloopr_list = [rloopr for rloopr in rloopr_generator]

        rloopr = adapters.rloopr.load_by_id(id=rloopr_list[0].id)
        assert isinstance(rloopr, RLoopr)

    @pytest.mark.skip(reason="Not implemented in production environment!")
    def test_rloopr_delete(self, adapters: Adapters) -> None:
        """It should delete rloopr analysis"""
        rloopr_generator = adapters.rloopr.load_all(tags=list())
        rloopr_list = [rloopr for rloopr in rloopr_generator]

        assert len(rloopr_list) == 1

        deleted: bool = adapters.rloopr.delete(id=rloopr_list[0].id)
        assert deleted is True
