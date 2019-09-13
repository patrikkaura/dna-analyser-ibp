import pytest
from pandas import DataFrame

from DNA_analyser_IBP.utils import generate_dataframe, validate_email


class TestUTils:

    @pytest.mark.parametrize(
        ["mail", "result"],
        [
            ("user@user.com", True),
            ("usr2faass.com", False),
            ("usr@fsakfa", False),
            ("@ffslak;fka/", False),
            ("usfasupiafuaspouafpuspaf@fopaifpaosifpaoifpsaiopf.cz", True),
            (".@.com", False),
            ("a.@a.com", True),
        ],
    )
    def test_email_validation(self, mail, result):
        """It should test if email is valid"""
        assert validate_email(mail) == result

    def test_generate_dataframe_dict(self):
        """It should test generating dataframe from dict."""
        dct = {"id": "somebulshit", "name": "idontknow", "ncbi": "20000"}
        data_frame = generate_dataframe(res=dct)
        assert isinstance(data_frame, DataFrame)
        assert data_frame.shape == (1, 3)

    def test_generate_dataframe_list_of_dicts(self):
        """It should test generating dataframe from list of dicts."""
        lst_of_dicts = [
            {"id": "somebulshit", "name": "idontknow", "ncbi": "20000"},
            {"id": "somebulshit", "name": "idontknow", "ncbi": "20000"},
            {"id": "somebulshit", "name": "idontknow", "ncbi": "20000"},
            {"id": "somebulshit", "name": "idontknow", "ncbi": "20000"},
        ]
        data_frame = generate_dataframe(res=lst_of_dicts)
        assert isinstance(data_frame, DataFrame)
        assert data_frame.shape == (4, 3)
