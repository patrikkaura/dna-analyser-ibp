from pandas import DataFrame

from DNA_analyser_IBP.models import G4Killer


def test_g4killer_model_creation_and_serialization() -> None:
    """It should create G4Killer model and pandas DataFrame."""

    g4_killer: G4Killer = G4Killer(
        originScore=1.2,
        changeCount=2,
        mutationScore=0.8,
        originSequence="ACACADABACAACACACA",
        onComplementary=True,
        targetThreshold=0.8,
        mutationSequences="ACACADABACAACACACA",
        mutationVariants="ACACADAB",
    )
    generated_dataframe: DataFrame = g4_killer.get_data_frame()

    # assert it genereta DataFrame
    assert isinstance(generated_dataframe, DataFrame)

    # value assertions
    assert generated_dataframe["origin_score"].iloc[0] == g4_killer.origin_score
    assert generated_dataframe["change_count"].iloc[0] == g4_killer.change_count
    assert generated_dataframe["mutation_score"].iloc[0] == g4_killer.mutation_score
    assert generated_dataframe["origin_sequence"].iloc[0] == g4_killer.origin_sequence
    assert generated_dataframe["on_complementary"].iloc[0] == g4_killer.on_complementary
    assert generated_dataframe["target_threshold"].iloc[0] == g4_killer.target_threshold
    assert (
        generated_dataframe["mutation_variants"].iloc[0] == g4_killer.mutation_variants
    )
    assert (
        generated_dataframe["mutation_sequences"].iloc[0]
        == g4_killer.mutation_sequences
    )
