# g4hunter_interface.py
# !/usr/bin/env python3

import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Union, Optional

from .analyse_interface import AnalyseInterface
from ..statusbar import status_bar
from ..callers import (
    User,
    G4HunterAnalyseFactory,
    G4HunterMethods
)
from ..utils import exception_handler, Logger, normalize_name


class G4Hunter(AnalyseInterface):
    """Api interface for g4hunter analyse caller"""

    def __init__(self, user: User):
        self.__user = user

    @exception_handler
    def load_all(self, tags: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Return all or filtered g4hunter analyses in dataframe

        Args:
            tags (Optional[List[str]]): tags for analyse filtering [default=None]

        Returns:
            pd.DataFrame: Dataframe with g4hunter analyses
        """
        g4 = [g4 for g4 in G4HunterMethods.load_all(user=self.__user, tags=tags if tags is not None else list())]
        data = pd.concat([g.get_dataframe() for g in g4], ignore_index=True)
        return data

    @exception_handler
    def load_by_id(self, *, id: str) -> pd.DataFrame:
        """
        Return g4hunter analyse in dataframe

        Args:
            id (str): g4hunter analyse id

        Returns:
            pd.DataFrame: Dataframe with g4hunter analyse
        """
        g4 = G4HunterMethods.load_by_id(user=self.__user, id=id)
        return g4.get_dataframe()

    @exception_handler
    def load_results(self, *, analyse: pd.Series) -> pd.DataFrame:
        """
        Return g4hunter analyses results in dataframe

        Args:
            analyse (pd.Series): g4hunter analyse series

        Returns:
            pd.DataFrame: Dataframe with g4hunter results
        """
        if isinstance(analyse, pd.Series):
            return G4HunterMethods.load_result(user=self.__user, id=analyse["id"])
        else:
            Logger.error("You have to insert pd.Series!")

    @exception_handler
    def get_heatmap(self, segments: Optional[int] = 31, coverage: Optional[bool] = False, *, analyse: pd.Series) -> pd.DataFrame:
        """
        Return dataframe with heatmap data

        Args:
            segments (Optional[int]): g4hunter analyse series [Default=31]
            coverage (Optional[bool]): True = coverage heatmap False = count heatmap [default=False]
            analyse (pd.Series): analyse series data to get heatmap

        Returns:
            pd.DataFrame: raw data used to create heatmap
        """
        if isinstance(analyse, pd.Series):
            return G4HunterMethods.load_heatmap(user=self.__user, id=analyse["id"], segments=segments)
        else:
            Logger.error("You have to insert pd.Series!")


    @exception_handler
    def show_heatmap(self, segments: Optional[int] = 31, coverage: Optional[bool] = False, *, analyse: pd.Series) -> None:
        """
        Return seaborn graph with heatmap

        Args:
            segments (Optional[int]): g4hunter analyse series [Default=31]
            coverage (Optional[bool]): True = coverage heatmap False = count heatmap [default=False]
            analyse (pd.Series): analyse series data to get heatmap

        Returns:
            pyplot: seaborn graph with g4hunter heatmap
        """
        if isinstance(analyse, pd.Series):
            data = G4HunterMethods.load_heatmap(user=self.__user, id=analyse["id"], segments=segments)
            graph = self._create_heatmap_grap(data=data, coverage=coverage)
            graph.grid(color="k", linestyle="-", linewidth=0.1)
            graph.show()
        else:
            Logger.error("You have to insert pd.Series!")

    @exception_handler
    def save_heatmap(self, segments: Optional[int] = 31, coverage: Optional[bool] = False, *, analyse: Union[pd.Series, pd.DataFrame], path: str):
        """
        Save seaborn graph with heatmap
        Args:
            segments (Optional[int]): g4hunter analyse series [Default=31]
            coverage (Optional[bool]): True = coverage heatmap False = count heatmap [default=False]
            analyse (Union[pd.Series, pd.DataFrame]): analyse series or analyses dataframe to get heatmap
            path (str): outputh path where to save heatmap SVGs
        """
        if isinstance(analyse, pd.DataFrame):
            for _, row in analyse.iterrows():
                data = G4HunterMethods.load_heatmap(user=self.__user, id=row["id"], segments=segments)
                graph = self._create_heatmap_grap(data=data, coverage=coverage)
                graph.savefig(f'{path}/{row["title"]}.svg', format="svg")
                graph.close()
                Logger.info(f'Heatmap file {row["title"]}.svg saved!')

        else:
            data = G4HunterMethods.load_heatmap(user=self.__user, id=analyse["id"], segments=segments)
            graph = self._create_heatmap_grap(data=data, coverage=coverage)
            graph.savefig(f'{path}/{analyse["title"]}.svg', format="svg")
            graph.close()
            Logger.info(f'Heatmap file {analyse["title"]}.svg saved!')

    @exception_handler
    def _create_heatmap_grap(self, *, data: pd.DataFrame, coverage: bool) -> plt:
        """
        Create heatmap graph for show|save
        Args:
            data (pd.DataFrame): dataframe used by pyplot
            coverage (bool): switch between coverate|count graph

        Returns:
            (plt): Matplotlib.pyplot graph object
        """
        ax = data[["PQS_coverage" if coverage else "PQS_count"]].plot(kind="bar", figsize=(14, 8), legend=True, fontsize=12)
        ax.set_xlabel("Segments", fontsize=12)
        ax.set_ylabel("PQS coverage [%/100]" if coverage else "PQS count [-]", fontsize=12)
        plt.grid(color="k", linestyle="-", linewidth=0.1)
        return plt

    @exception_handler
    def analyse_creator(self, tags: Optional[List[str]] = None, *, sequence: Union[pd.DataFrame, pd.Series], threshold: float, window_size: int) -> None:
        """
        Create G4hunter analyse

        Args:
            tags (Optional[List[str]]): tags for analyse filtering [default=None]
            sequence (Union[pd.DataFrame, pd.Series]): one or many sequences to analyse
            threshold (float): g4hunter threshold recommended 1.2
            window_size (int): g4hunter window size recommended 25
        """
        # start g4hunter analyse factory
        if isinstance(sequence, pd.DataFrame):
            for _, row in sequence.iterrows():
                name = normalize_name(row["name"])
                status_bar(user=self.__user, func=lambda: G4HunterAnalyseFactory(
                    user=self.__user,
                    id=row["id"],
                    tags=self._process_tags(tags, row['tags']),
                    threshold=threshold,
                    window_size=window_size,
                ), name=name, cls_switch=False)
        else:
            name = normalize_name(sequence["name"])
            status_bar(user=self.__user, func=lambda: G4HunterAnalyseFactory(
                user=self.__user,
                id=sequence["id"],
                tags=self._process_tags(tags, sequence['tags']),
                threshold=threshold,
                window_size=window_size,
            ), name=name, cls_switch=False)

    @staticmethod
    def _process_tags(tags: List[str], sequence_tags: str) -> List[Optional[str]]:
        """
        Return original tags|strip tags from sequence dataframe or return empty list()

        Args:
            tags List(str): tags given as function parameter
            sequence_tags (str): sequence dataframe tags

        Returns:
            List[Optional[str]]:
        """
        if tags is not None:
            return tags
        elif sequence_tags:
            return [tag.strip() for tag in sequence_tags.split(',')]
        return list()

    @exception_handler
    def export_csv(self, *, analyse: Union[pd.DataFrame, pd.Series], path: str, aggregate: bool = True) -> None:
        """
        Export G4Hunter analyses result into csv files

        Args:
            analyse (Union[pd.DataFrame, pd.Series]): g4hunter analyse Dataframe|Series
            path (str): absolute system path to output folder
            aggregate (bool): True = aggregation, False = no aggregation
        """
        if isinstance(analyse, pd.Series):
            _id = analyse["id"]
            name = normalize_name(analyse["title"])
            file_path = os.path.join(path, f"{name}_{_id}.csv")

            with open(file_path, "w") as new_file:
                data = G4HunterMethods.export_csv(user=self.__user, id=_id, aggregate=aggregate)
                new_file.write(data)
            Logger.info(f"file created -> {file_path}")
        # export multiple analyses
        else:
            for _, row in analyse.iterrows():
                _id = row["id"]
                name = normalize_name(row["title"])
                file_path = os.path.join(path, f"{name}_{_id}.csv")

                with open(file_path, "w") as new_file:
                    data = G4HunterMethods.export_csv(user=self.__user, id=_id, aggregate=aggregate)
                    new_file.write(data)
                Logger.info(f"file created -> {file_path}")

    @exception_handler
    def delete(self, *, analyse: Union[pd.DataFrame, pd.Series]) -> None:
        """
        Delete G4Hunter analyse

        Args:
            analyse (Union[pd.DataFrame, pd.Series]): g4hunter analyse [Dataframe|Series]
        """
        if isinstance(analyse, pd.DataFrame):
            for _, row in analyse.iterrows():
                _id = row["id"]
                if G4HunterMethods.delete(user=self.__user, id=_id):
                    Logger.info(f"G4hunter analyse {_id} was deleted!")
                    time.sleep(1)
                else:
                    Logger.error(f"G4hunter analyse {_id} cannot be deleted!")
        else:
            _id = analyse["id"]
            if G4HunterMethods.delete(user=self.__user, id=_id):
                Logger.info(f"G4hunter analyse {_id} was deleted!")
            else:
                Logger.error(f"G4hunter analyse {_id} cannot be deleted!")
