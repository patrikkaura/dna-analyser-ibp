from pandas import DataFrame

from DNA_analyser_IBP.models import G4Hunter


def test_g4hunter_model_creation_and_serialization() -> None:
    """It should create G4Hunter model and pandas DataFrame."""

    nucleic_count = {"A": 20, "T": 1, "C": 12}

    g4hunter: G4Hunter = G4Hunter(
        id="id",
        title="title",
        tags=["test"],
        created="20-20-2020",
        finished="20-20-2020",
        sequenceId="test",
        resultCount=20,
        threshold=1.2,
        frequency=2,
        windowSize=25,
    )
    generated_dataframe: DataFrame = g4hunter.get_data_frame()

    # assert it genereta DataFrame
    assert isinstance(generated_dataframe, DataFrame)

    # value assertions
    assert generated_dataframe["id"].iloc[0] == g4hunter.id
    assert generated_dataframe["tags"].iloc[0] == g4hunter.tags
    assert generated_dataframe["title"].iloc[0] == g4hunter.title
    assert generated_dataframe["created"].iloc[0] == g4hunter.created
    assert generated_dataframe["finished"].iloc[0] == g4hunter.finished
    assert generated_dataframe["threshold"].iloc[0] == g4hunter.threshold
    assert generated_dataframe["frequency"].iloc[0] == g4hunter.frequency
    assert generated_dataframe["sequence_id"].iloc[0] == g4hunter.sequence_id
    assert generated_dataframe["window_size"].iloc[0] == g4hunter.window_size
    assert generated_dataframe["result_count"].iloc[0] == g4hunter.result_count
