from pandas import DataFrame

from DNA_analyser_IBP.models import Batch


def test_batch_model_creation_and_serialization() -> None:
    """It should create Batch model and pandas DataFrame."""

    batch: Batch = Batch(
        cpuTime=123132132132,
        created="20-20-2020",
        exception="NONE",
        finished="20-20-2020",
        name="batch.sequence.test",
        progress=20,
        started="20-20-2020",
        status="FINISH",
    )
    generated_dataframe: DataFrame = batch.get_data_frame()

    # assert it genereta DataFrame
    assert isinstance(generated_dataframe, DataFrame)

    # value assertions
    assert generated_dataframe["cpu_time"].iloc[0] == batch.cpu_time
    assert generated_dataframe["created"].iloc[0] == batch.created
    assert generated_dataframe["exception"].iloc[0] == batch.exception
    assert generated_dataframe["finished"].iloc[0] == batch.finished
    assert generated_dataframe["name"].iloc[0] == batch.name
    assert generated_dataframe["progress"].iloc[0] == batch.progress
    assert generated_dataframe["started"].iloc[0] == batch.started
    assert generated_dataframe["status"].iloc[0] == batch.status
