from pandas import DataFrame

from DNA_analyser_IBP.models import Sequence


def test_sequence_model_creation_and_serialization() -> None:
    """It should create Sequence model and pandas DataFrame."""

    nucleic_count = {"A": 20, "T": 1, "C": 12}

    sequence: Sequence = Sequence(
        id="id",
        name="name",
        type="DNA",
        tags=["test", "test"],
        length=20,
        circular=True,
        created="20-20-2020",
        ncbi="NC123",
        fastaComment="TEEEEEEEEST",
        nucleicCounts=nucleic_count,
    )
    generated_dataframe: DataFrame = sequence.get_data_frame()

    # assert it genereta DataFrame
    assert isinstance(generated_dataframe, DataFrame)

    # value assertions
    assert generated_dataframe["id"].iloc[0] == sequence.id
    assert generated_dataframe["name"].iloc[0] == sequence.name
    assert generated_dataframe["type"].iloc[0] == sequence.type
    assert generated_dataframe["tags"].iloc[0] == sequence.tags
    assert generated_dataframe["length"].iloc[0] == sequence.length
    assert generated_dataframe["circular"].iloc[0] == sequence.circular
    assert generated_dataframe["created"].iloc[0] == sequence.created
    assert generated_dataframe["ncbi"].iloc[0] == sequence.ncbi
    assert generated_dataframe["fasta_comment"].iloc[0] == sequence.fasta_comment
    assert generated_dataframe["nucleic_count"].iloc[0] == str(nucleic_count)
    assert generated_dataframe["gc_count"].iloc[0] == nucleic_count["C"]  # 12
