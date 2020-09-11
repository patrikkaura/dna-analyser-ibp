from pandas import DataFrame

from DNA_analyser_IBP.models import RLoopr


def test_rloopr_model_creation_and_serialization() -> None:
    """It should create RLoopr model and pandas DataFrame."""

    rloopr: RLoopr = RLoopr(
        id="id",
        title="title",
        tags=["test"],
        created="20-20-2020",
        finished="20-20-2020",
        sequenceId="test",
        model=3,
        resultCount=20,
    )
    generated_dataframe: DataFrame = rloopr.get_data_frame()

    # assert it genereta DataFrame
    assert isinstance(generated_dataframe, DataFrame)

    # value assertions
    assert generated_dataframe["id"].iloc[0] == rloopr.id
    assert generated_dataframe["tags"].iloc[0] == rloopr.tags
    assert generated_dataframe["title"].iloc[0] == rloopr.title
    assert generated_dataframe["model"].iloc[0] == rloopr.model
    assert generated_dataframe["created"].iloc[0] == rloopr.created
    assert generated_dataframe["finished"].iloc[0] == rloopr.finished
    assert generated_dataframe["sequence_id"].iloc[0] == rloopr.sequence_id
    assert generated_dataframe["result_count"].iloc[0] == rloopr.result_count
