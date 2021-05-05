# g4hunter_interface.py

import os
import time
from typing import List, Optional, Union

import matplotlib.pyplot as plt
import pandas as pd

from DNA_analyser_IBP.interfaces.analyse_interface import AnalyseInterface
from DNA_analyser_IBP.models import G4Hunter as Analyse
from DNA_analyser_IBP.ports import Ports
from DNA_analyser_IBP.statusbar import status_bar
from DNA_analyser_IBP.type import Types
from DNA_analyser_IBP.utils import Logger, exception_handler, normalize_name


class G4Hunter(AnalyseInterface):
    """Api interface for g4hunter analyse caller"""

    def __init__(self, ports: Ports):
        self.__ports = ports

    @exception_handler
    def load_all(self, tags: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Return all or filtered g4hunter analyses in DataFrame

        Args:
            tags (Optional[List[str]]): tags for analyse filtering [default=None]

        Returns:
            pd.DataFrame: DataFrame with g4hunter analyses
        """
        listed_g4hunter: list = [
            g4hunter
            for g4hunter in self.__ports.g4hunter.load_all(
                tags=tags if tags is not None else list()
            )
        ]
        data: pd.DataFrame = pd.concat(
            [g4hunter.get_data_frame() for g4hunter in listed_g4hunter],
            ignore_index=True,
        )

        return data

    @exception_handler
    def load_by_id(self, *, id: str) -> pd.DataFrame:
        """
        Return g4hunter analyse in DataFrame

        Args:
            id (str): g4hunter analyse id

        Returns:
            pd.DataFrame: DataFrame with g4hunter analyse
        """
        g4hunter: Analyse = self.__ports.g4hunter.load_by_id(id=id)

        return g4hunter.get_data_frame()

    @exception_handler
    def load_results(self, *, analyse: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        """
        Return g4hunter analyses results in DataFrame

        Args:
            analyse (Union[pd.Series, pd.DataFrame]): g4hunter analyse

        Returns:
            pd.DataFrame: DataFrame with g4hunter results
        """
        if isinstance(analyse, pd.Series):
            return self.__ports.g4hunter.load_result(id=analyse["id"])
        elif isinstance(analyse, pd.DataFrame):
            return self.__ports.g4hunter.load_result(id=analyse.iloc[0]["id"])
        else:
            Logger.error("You have to insert pd.Series or pd.DataFrame!")

    @exception_handler
    def get_heatmap_data(
        self,
        segments: Optional[int] = 31,
        *,
        analyse: Union[pd.Series, pd.DataFrame],
    ) -> pd.DataFrame:
        """
        Return DataFrame with heatmap data

        Args:
            segments (Optional[int]): g4hunter analyse series [Default=31]
            analyse (Union[pd.Series, pd.DataFrame]): analyse series data to get heatmap

        Returns:
            pd.DataFrame: raw data used to create heatmap
        """
        if isinstance(analyse, pd.Series):
            return self.__ports.g4hunter.load_heatmap(
                id=analyse["id"], segments=segments
            )
        else:
            Logger.error("You have to insert pd.Series!")

    @exception_handler
    def show_heatmap(
        self,
        segments: Optional[int] = 31,
        coverage: Optional[bool] = False,
        *,
        analyse: Union[pd.Series, pd.DataFrame],
    ) -> None:
        """
        Return Seaborn graph with heatmap

        Args:
            segments (Optional[int]): g4hunter analyse series [Default=31]
            coverage (Optional[bool]): True = coverage heatmap False = count heatmap [default=False]
            analyse (Union[pd.Series, pd.DataFrame]): analyse series data to get heatmap

        Returns:
            pyplot: Seaborn graph with g4hunter heatmap
        """

        def _show_heatmap(*, _id: str) -> None:
            data: pd.DataFrame = self.__ports.g4hunter.load_heatmap(
                id=_id, segments=segments
            )
            graph: plt = self._create_heatmap_graph(data=data, coverage=coverage)
            graph.grid(color="k", linestyle="-", linewidth=0.1)
            graph.show()

        if isinstance(analyse, pd.DataFrame):
            return _show_heatmap(_id=analyse.iloc[0]["id"])
        elif isinstance(analyse, pd.Series):
            return _show_heatmap(_id=analyse["id"])
        else:
            Logger.error("You have to insert pd.Series!")

    @exception_handler
    def save_heatmap(
        self,
        segments: Optional[int] = 31,
        coverage: Optional[bool] = False,
        *,
        analyse: Union[pd.Series, pd.DataFrame],
        path: str,
    ):
        """
        Save Seaborn graph with heatmap
        Args:
            segments (Optional[int]): g4hunter analyse series [Default=31]
            coverage (Optional[bool]): True = coverage heatmap False = count heatmap [default=False]
            analyse (Union[pd.Series, pd.DataFrame]): analyse series or analyses dataframe to get heatmap
            path (str): output path where to save heatmap SVGs
        """

        def _save_heatmap(id: str, name: str) -> None:
            data = self.__ports.g4hunter.load_heatmap(id=id, segments=segments)
            graph: plt = self._create_heatmap_graph(data=data, coverage=coverage)
            graph.savefig(f"{path}/{name}.svg", format="svg")
            graph.close()
            Logger.info(f"Heatmap file {name}.svg saved!")

        if isinstance(analyse, pd.DataFrame):
            for _, row in analyse.iterrows():
                _save_heatmap(id=row["id"], name=row["title"])
        else:
            _save_heatmap(id=analyse["id"], name=analyse["title"])

    @exception_handler
    def _create_heatmap_graph(self, *, data: pd.DataFrame, coverage: bool) -> plt:
        """
        Create heatmap graph for quick view | save
        Args:
            data (pd.DataFrame): DataFrane used by pyplot
            coverage (bool): switch between coverate|count graph

        Returns:
            (plt): Matplotlib.pyplot graph object
        """
        ax = data[["PQS_coverage" if coverage else "PQS_count"]].plot(
            kind="bar", figsize=(14, 8), legend=True, fontsize=12
        )
        ax.set_xlabel("Segments", fontsize=12)
        ax.set_ylabel(
            "PQS coverage [%/100]" if coverage else "PQS count [-]", fontsize=12
        )
        plt.grid(color="k", linestyle="-", linewidth=0.1)
        return plt

    @exception_handler
    def analyse_creator(
        self,
        tags: Optional[List[str]] = None,
        *,
        sequence: Union[pd.DataFrame, pd.Series],
        threshold: float,
        window_size: int,
    ) -> None:
        """
        Create G4hunter analyse

        Args:
            tags (Optional[List[str]]): tags for analyse filtering [default=None]
            sequence (Union[pd.DataFrame, pd.Series]): one or many sequences to analyse
            threshold (float): g4hunter threshold recommended 1.2
            window_size (int): g4hunter window size recommended 25
        """

        def _analyse_creator(id: str, name: str, tags: List[Optional[str]]) -> None:
            name: str = normalize_name(name)
            status_bar(
                ports=self.__ports,
                func=lambda: self.__ports.g4hunter.create_analyse(
                    id=id,
                    tags=tags,
                    threshold=threshold,
                    window_size=window_size,
                ),
                name=name,
                type=Types.G4HUNTER,
            )

        if isinstance(sequence, pd.DataFrame):
            for _, row in sequence.iterrows():
                _tags = self._process_tags(tags, row["tags"])
                _analyse_creator(id=row["id"], name=row["name"], tags=_tags)
        else:
            _tags = self._process_tags(tags, sequence["tags"])
            _analyse_creator(id=sequence["id"], name=sequence["name"], tags=_tags)

    @staticmethod
    def _process_tags(tags: List[str], sequence_tags: str) -> List[Optional[str]]:
        """
        Return original tags|strip tags from sequence DataFrame or return empty list()

        Args:
            tags List(str): tags given as function parameter
            sequence_tags (str): sequence DataFrame tags

        Returns:
            List[Optional[str]]:
        """
        if tags is not None:
            return tags
        elif sequence_tags:
            return [tag.strip() for tag in sequence_tags.split(",")]
        return list()

    @exception_handler
    def export_csv(
        self,
        *,
        analyse: Union[pd.DataFrame, pd.Series],
        path: str,
        aggregate: bool = True,
    ) -> None:
        """
        Export G4Hunter analyses result into csv files

        Args:
            analyse (Union[pd.DataFrame, pd.Series]): g4hunter analyse DataFrame|Series
            path (str): absolute system path to output folder
            aggregate (bool): True = aggregation, False = no aggregation
        """

        def _export_csv(id: str, name: str) -> None:
            name: str = normalize_name(name=name)
            file_path: str = os.path.join(path, f"{name}_{id}_result.csv")

            with open(file_path, "w") as new_file:
                data: str = self.__ports.g4hunter.export_csv(id=id, aggregate=aggregate)
                new_file.write(data)
            Logger.info(f"file created -> {file_path}")

        if isinstance(analyse, pd.DataFrame):
            for _, row in analyse.iterrows():
                _export_csv(id=row["id"], name=row["title"])
        else:
            _export_csv(id=analyse["id"], name=analyse["title"])

    @exception_handler
    def delete(self, *, analyse: Union[pd.DataFrame, pd.Series]) -> None:
        """
        Delete G4Hunter analyse

        Args:
            analyse (Union[pd.DataFrame, pd.Series]): g4hunter analyse [DataFrame|Series]
        """

        def _delete(id: str) -> None:
            if self.__ports.g4hunter.delete(id=id):
                Logger.info(f"G4hunter analyse {id} was deleted!")
                time.sleep(1)
            else:
                Logger.error(f"G4hunter analyse {id} cannot be deleted!")

        if isinstance(analyse, pd.DataFrame):
            for _, row in analyse.iterrows():
                _delete(id=row["id"])
        else:
            _delete(id=analyse["id"])
