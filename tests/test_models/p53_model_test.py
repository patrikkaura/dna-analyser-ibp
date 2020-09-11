from pandas import DataFrame

from DNA_analyser_IBP.models import P53


def test_p53_model_creation_and_serialization() -> None:
    """It should create P53 model and pandas DataFrame."""

    p53_predictor: P53 = P53(
        sequence="ACACADABACAACACACA",
        affinity=1.2,
        predictor=5,
        difference=2,
        length=20,
        position=10,
    )
    generated_dataframe: DataFrame = p53_predictor.get_data_frame()

    # assert it genereta DataFrame
    assert isinstance(generated_dataframe, DataFrame)

    # value assertions
    assert generated_dataframe["sequence"].iloc[0] == p53_predictor.sequence
    assert generated_dataframe["affinity"].iloc[0] == p53_predictor.affinity
    assert generated_dataframe["predictor"].iloc[0] == p53_predictor.predictor
    assert generated_dataframe["difference"].iloc[0] == p53_predictor.difference
    assert generated_dataframe["length"].iloc[0] == p53_predictor.length
    assert generated_dataframe["position"].iloc[0] == p53_predictor.position
