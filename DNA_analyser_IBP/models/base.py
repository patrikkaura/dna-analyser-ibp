# base.py

from pandas import DataFrame


class Base:
    """
    Base model
    """

    def get_data_frame(self) -> DataFrame:
        """
        Return pandas DataFrame for current object

        Returns:
            pd.DataFrame: DataFrame with object data
        """
        data_frame: DataFrame = DataFrame().from_records(
            self.__dict__, columns=self.__dict__.keys(), index=[0]
        )
        return data_frame
