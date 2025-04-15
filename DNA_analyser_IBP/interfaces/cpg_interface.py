# cpg_interface.py

import os
import time
from typing import List, Optional, Union

import pandas as pd

from DNA_analyser_IBP.interfaces.analyse_interface import AnalyseInterface
from DNA_analyser_IBP.models import CpG as Analyse
from DNA_analyser_IBP.ports import Ports
from DNA_analyser_IBP.statusbar import status_bar
from DNA_analyser_IBP.type import Types
from DNA_analyser_IBP.utils import Logger, exception_handler, normalize_name

class CpG(AnalyseInterface):
    """
    Api interface for cpg analyse
    """

    def __init__(self, ports: Ports):
        self.__ports: Ports = ports

    @exception_handler
    def analyse_creator(self, 
        tags: Optional[List[str]] = None,
        min_window_size: Optional[int] = 200,
        *,
        min_gc_percentage: Optional[float] = 0.5,
        min_obs_exp_cpg: Optional[float] = 0.6,
        min_island_merge_gap: Optional[int] = 100,
        second_nucleotide: Optional[str] = "G",
        sequence = Union[pd.DataFrame, pd.Series]) -> None:
        """
        Create CpG Hunter analyse

        Args:
            tags (Optional[List[str]]): tags for analyse filtering [default=None],
            sequence (Union[pd.DataFrame, pd.Series]): one or many sequences to analyse,
            min_window_size (Optional[int]): 
            min_gc_percentage (Optional[float]):
            min_obs_exp_cpg (Optional[float]):
            min_island_merge_gap (Optional[int]):
            second_nucleotide (Optional[str]):
        """
        
        def _analyse_creator(id: str, name: str, tags: List[Optional[str]]) -> None:
            status_bar(
                ports=self.__ports,
                func=lambda: self.__ports.cpg.create_analyse(
                    id=id,
                    tags=tags,
                    min_window_size=min_window_size,
                    min_gc_percentage=min_gc_percentage,
                    min_obs_exp_cpg=min_obs_exp_cpg,
                    min_island_merge_gap=min_island_merge_gap,
                    second_nucleotide=second_nucleotide,
                ),
                name=normalize_name(name),
                type=Types.CPG,
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
    def load_all(self, tags: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Return all or filtered cpg analyses in DataFrame

        Args:
            tags (Optional[List[str]]): tags for analyse filtering [default=None]

        Returns:
            pd.DataFrame: DataFrame with cpg analyses
        """
        listed_cpg: list = [
            cpg for cpg in self.__ports.cpg.load_all(
                tags=tags if tags is not None else list()
            )
        ]

        data: pd.DataFrame = pd.concat(
            [g4hunter.get_data_frame() for g4hunter in listed_cpg],
            ignore_index=True,
        )

        return data
    
    @exception_handler
    def load_by_id(self, *, id: str) -> pd.DataFrame:
        """
        Return cpg hunter analyse in DataFrame

        Args:
            id (str): cpg hunter analyse id

        Returns:
            pd.DataFrame: DataFrame with cpg hunter analyse
        """
        cpg: Analyse = self.__ports.cpg.load_by_id(id=id)

        return cpg.get_data_frame()
    
    @exception_handler
    def delete(self, *, analyse: Union[pd.DataFrame, pd.Series]) -> None:
        """
        Delete CpG analyse

        Args:
            analyse (Union[pd.DataFrame, pd.Series]): cpg analyse [DataFrame|Series]
        """

        def _delete(id: str) -> None:
            if self.__ports.cpg.delete(id=id):
                Logger.info(f"CpG analyse {id} was deleted!")
                time.sleep(1)
            else:
                Logger.error(f"CpG analyse {id} cannot be deleted!")

        if isinstance(analyse, pd.DataFrame):
            for _, row in analyse.iterrows():
                _delete(id=row["id"])
        else:
            _delete(id=analyse["id"])

    @exception_handler
    def export_csv(
        self,
        *,
        analyse: Union[pd.DataFrame, pd.Series],
        path: str,
    ) -> None:
        """
        Export CpX analyses result into csv files

        Args:
            analyse (Union[pd.DataFrame, pd.Series]): g4hunter analyse DataFrame|Series
            path (str): absolute system path to output folder
        """

        def _export_csv(id: str, name: str) -> None:
            name: str = normalize_name(name=name)
            file_path: str = os.path.join(path, f"{name}_result.csv")

            with open(file_path, "w") as new_file:
                data: str = self.__ports.cpg.export_csv(id=id)
                new_file.write(data)
            Logger.info(f"file created -> {file_path}")

        if isinstance(analyse, pd.DataFrame):
            for _, row in analyse.iterrows():
                _export_csv(id=row["id"], name=row["title"])
        else:
            _export_csv(id=analyse["id"], name=analyse["title"])

    @exception_handler
    def load_results(self, *, analyse: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        """
        Return cpg analyses results in DataFrame

        Args:
            analyse (Union[pd.Series, pd.DataFrame]): cpg analyse

        Returns:
            pd.DataFrame: DataFrame with cpg hunter results
        """
        if isinstance(analyse, pd.Series):
            return self.__ports.cpg.load_result(id=analyse["id"])
        elif isinstance(analyse, pd.DataFrame):
            return self.__ports.cpg.load_result(id=analyse.iloc[0]["id"])
        else:
            Logger.error("You have to insert pd.Series or pd.DataFrame!")