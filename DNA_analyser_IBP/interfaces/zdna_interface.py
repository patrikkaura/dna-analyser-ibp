# zdna_interface.py

import os
import time
from typing import List, Optional, Union, Dict

import matplotlib.pyplot as plt
import pandas as pd

from DNA_analyser_IBP.interfaces.analyse_interface import AnalyseInterface
from DNA_analyser_IBP.models import ZDna as Analyse
from DNA_analyser_IBP.ports import Ports
from DNA_analyser_IBP.statusbar import status_bar
from DNA_analyser_IBP.type import Types
from DNA_analyser_IBP.utils import Logger, exception_handler, normalize_name

class ZDna(AnalyseInterface):

    def __init__(self, ports: Ports):
        self.__ports = ports

    
    @exception_handler
    def analyse_creator(
        self,
        tags: Optional[List[str]] = None,
        *,
        min_sequence_size: int = 10,
        model: Optional[List[str]] = "model1",
        GC_score: float = 25,
        GTAC_score: float = 3,
        AT_score: float = 0,
        oth_score: float = 0,
        min_score_percentage: float = 12,
        sequence: Union[pd.DataFrame, pd.Series],
    ) -> None:
        """
        Create z-dna analyse

        Args:
            tags (Optional[List[str]]): tags for analyse filtering [default=None]
            sequence (Union[pd.DataFrame, pd.Series]): one or many sequences to analyse
        
        
        _model_defaults: Dict = {
            "model1": {"GC_score": 25, "GTAC_score": 3, "AT_score": 0, "min_score_percentage": 12},
            "model2": {"GC_score": 2, "GTAC_score": 1, "AT_score": 0.5, "min_score_percentage": 50},
        }

        # setting default argument values based on model settings
        selected_model = model[0] if isinstance(model, list) and model else "model1"
        defaults = _model_defaults.get(selected_model, _model_defaults["model1"])
        
        for arg in [GC_score, GTAC_score, AT_score, min_score_percentage]:
            arg = arg if arg is not None else defaults["{arg}"]
        """

        def _analyse_creator(id: str, name: str, tags: List[Optional[str]]) -> None:
            name: str = normalize_name(name)
            status_bar(
                ports=self.__ports,
                func=lambda: self.__ports.zdna.create_analyse(
                    id=id,
                    tags=tags,
                    min_sequence_size=min_sequence_size,
                    model=self._process_prediction_models(model=model) if model not in ["model1", "model2"] else model,
                    GC_score=GC_score,
                    GTAC_score=GTAC_score,
                    AT_score=AT_score,
                    oth_score=oth_score,
                    min_score_percentage=min_score_percentage,
                ),
                name=name,
                type=Types.ZDNA,
            )

        if isinstance(sequence, pd.DataFrame):
            for _, row in sequence.iterrows():
                _tags = self._process_tags(tags, row["tags"])
                _analyse_creator(id=row["id"], name=row["name"], tags=_tags)
        else:
            _tags = self._process_tags(tags, sequence["tags"])
            _analyse_creator(id=sequence["id"], name=sequence["name"], tags=_tags)

    @staticmethod
    def _process_prediction_models(*, model: str) -> str:
        """
        Args:
            model (str): "1" or "2"

        Returns:
            model_id (str): model tag ("model1" or "model2")
        """

        model_tag: str
        if model == "1":
            model_tag = "model1"
        elif model == "2":
            model_tag = "model2"
        else:
            Logger.error("Model number could not be resolved!")
            return None

        return model_tag

    @exception_handler
    def load_all(self, tags: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Return all or filtered z-dna hunter analyses in DataFrame

        Args:
            tags (Optional[List[str]]): tags for analyse filtering [default=None]

        Returns:
            pd.DataFrame: DataFrame with z-dna hunter analyses
        """
        listed_zdna: list = [
            zdna
            for zdna in self.__ports.zdna.load_all(
                tags=tags if tags is not None else list()
            )
        ]
        data: pd.DataFrame = pd.concat(
            [zdna.get_data_frame() for zdna in listed_zdna],
            ignore_index=True,
        )

        return data
    
    @exception_handler
    def load_by_id(self, *, id: str) -> pd.DataFrame:
        """
        Return z-dna hunter analyse in DataFrame

        Args:
            id (str): z-dna hunter analyse id

        Returns:
            pd.DataFrame: DataFrame with z-dna hunter analyse
        """
        zdna: Analyse = self.__ports.zdna.load_by_id(id=id)

        return zdna.get_data_frame()
    
    @exception_handler
    def load_results(self, *, analyse: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        """
        Return z-dna analyses results in DataFrame

        Args:
            analyse (Union[pd.Series, pd.DataFrame]): z-dna analyse

        Returns:
            pd.DataFrame: DataFrame with z-dna results
        """
        if isinstance(analyse, pd.Series):
            return self.__ports.zdna.load_result(id=analyse["id"])
        elif isinstance(analyse, pd.DataFrame):
            return self.__ports.zdna.load_result(id=analyse.iloc[0]["id"])
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
            segments (Optional[int]): z-dna analyse series [Default=31]
            analyse (Union[pd.Series, pd.DataFrame]): analyse series data to get heatmap

        Returns:
            pd.DataFrame: raw data used to create heatmap
        """
        if isinstance(analyse, pd.Series):
            return self.__ports.zdna.load_heatmap(
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
            segments (Optional[int]): z-dna analyse series [Default=31]
            coverage (Optional[bool]): True = coverage heatmap False = count heatmap [default=False]
            analyse (Union[pd.Series, pd.DataFrame]): analyse series data to get heatmap

        Returns:
            pyplot: Seaborn graph with z-dna heatmap
        """

        def _show_heatmap(*, _id: str) -> None:
            data: pd.DataFrame = self.__ports.zdna.load_heatmap(
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
            segments (Optional[int]): z-dna analyse series [Default=31]
            coverage (Optional[bool]): True = coverage heatmap False = count heatmap [default=False]
            analyse (Union[pd.Series, pd.DataFrame]): analyse series or analyses dataframe to get heatmap
            path (str): output path where to save heatmap SVGs
        """

        def _save_heatmap(id: str, name: str) -> None:
            data = self.__ports.zdna.load_heatmap(id=id, segments=segments)
            graph: plt = self._create_heatmap_graph(data=data, coverage=coverage)
            graph.savefig(f"{path}/{name}.svg", format="svg")
            graph.close()
            Logger.info(f"Heatmap file {name}.svg saved!")

        if isinstance(analyse, pd.DataFrame):
            for _, row in analyse.iterrows():
                _save_heatmap(id=row["id"], name=row["title"])
        else:
            _save_heatmap(id=analyse["id"], name=analyse["title"])

    
    # funkci nize upravit pro z-dna -> (done)

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
        ax = data[["Z-DNA_coverage" if coverage else "Z-DNA_count"]].plot(
            kind="bar", figsize=(14, 8), legend=True, fontsize=12
        )
        ax.set_xlabel("Segments", fontsize=12)
        ax.set_ylabel(
            "Z-DNA coverage [%/100]" if coverage else "Z-DNA count [-]", fontsize=12
        )
        plt.grid(color="k", linestyle="-", linewidth=0.1)
        return plt

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
    ) -> None:
        """
        Export z-dna analyses result into csv files

        Args:
            analyse (Union[pd.DataFrame, pd.Series]): z-dna analyse DataFrame|Series
            path (str): absolute system path to output folder
        """

        def _export_csv(id: str, name: str) -> None:
            name: str = normalize_name(name=name)
            file_path: str = os.path.join(path, f"{name}_{id}_result.csv")

            with open(file_path, "w") as new_file:
                data: str = self.__ports.zdna.export_csv(id=id)
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
        Delete z-dna analyse

        Args:
            analyse (Union[pd.DataFrame, pd.Series]): z-dna analyse [DataFrame|Series]
        """

        def _delete(id: str) -> None:
            if self.__ports.zdna.delete(id=id):
                Logger.info(f"z-dna analyse {id} was deleted!")
                time.sleep(1)
            else:
                Logger.error(f"z-dna analyse {id} cannot be deleted!")

        if isinstance(analyse, pd.DataFrame):
            for _, row in analyse.iterrows():
                _delete(id=row["id"])
        else:
            _delete(id=analyse["id"])
