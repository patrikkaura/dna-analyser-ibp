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
    g4_delete_analyse,
    g4_export_csv,
    g4_load_all,
    g4_load_by_id,
    g4_load_result,
    g4_load_heatmap,
)


class G4Hunter(AnalyseInterface):
    """Api interface for g4hunter analyse caller"""

    def __init__(self, user: User):
        self.__user = user

    def load_all(self, filter_tag: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Return all or filtered g4hunter analyses in dataframe
        :param filter_tag: tags for analyse filtering [default=None]
        :return: dataframe with g4hunter analyses
        """
        g4 = [g4 for g4 in g4_load_all(user=self.__user, filter_tag=filter_tag if filter_tag is not None else list())]
        data = pd.concat([g.get_dataframe() for g in g4], ignore_index=True)
        return data

    def load_by_id(self, *, id: str) -> pd.DataFrame:
        """
        Return g4hunter analyses in dataframe
        :param id: g4hunter analyse id
        :return: dataframe with g4hunter analyse
        """
        g4 = g4_load_by_id(user=self.__user, id=id)
        return g4.get_dataframe()

    def load_results(self, *, g4hunter_analyse: pd.Series) -> pd.DataFrame:
        """
        Return g4hunter analyses results in dataframe
        :param g4hunter_analyse: g4hunter analyse series
        :return: dataframe with g4hunter results
        """
        if isinstance(g4hunter_analyse, pd.Series):
            return g4_load_result(user=self.__user, id=g4hunter_analyse["id"])
        else:
            raise ("You have to insert pd.Series")

    def load_heatmap(self, segment_count: Optional[int] = 31, coverage: Optional[bool] = False, *, g4hunter_analyse: pd.Series) -> None:
        """
        Return seaborn graph with heatmap
        :param g4hunter_analyse: g4hunter analyse series
        :param segment_count: number of heatmap segments [default=31]
        :param coverage: True = coverage heatmap False = count heatmap [default=False]
        :return: seaborn graph with g4hunter heatmap
        """
        if isinstance(g4hunter_analyse, pd.Series):
            data = g4_load_heatmap(user=self.__user, id=g4hunter_analyse["id"], segment_count=segment_count)
            ax = data[["coverage" if coverage else "count"]].plot(kind="bar", figsize=(14, 8), legend=True, fontsize=12)
            ax.set_xlabel("segments", fontsize=12)
            ax.set_ylabel("coverage [%/100]" if coverage else "count [-]", fontsize=12)
            plt.grid(color="k", linestyle="-", linewidth=0.1)
            plt.show()
        else:
            raise ("You have to insert pd.Series")

    def analyse_creator(self, tags: Optional[List[str]] = None, *, sequence: Union[pd.DataFrame, pd.Series], threshold: float, window_size: int) -> None:
        """
        Create G4hunter analyse
        :param sequence: one or many sequences to analyse
        :param tags: tags for analyse filtering [default=None]
        :param threshold: g4hunter threshold recommended 1.2
        :param window_size: g4hunter window size recommended 25
        :return:
        """
        # start g4hunter analyse factory
        if isinstance(sequence, pd.DataFrame):
            for _, row in sequence.iterrows():
                status_bar(user=self.__user, func=lambda: G4HunterAnalyseFactory(
                    user=self.__user,
                    id=row["id"],
                    tags=self._process_tags(tags, row['tags']),
                    threshold=threshold,
                    window_size=window_size,
                ), name=row["name"], cls_switch=False)
        else:
            status_bar(user=self.__user, func=lambda: G4HunterAnalyseFactory(
                user=self.__user,
                id=sequence["id"],
                tags=self._process_tags(tags, sequence['tags']),
                threshold=threshold,
                window_size=window_size,
            ), name=sequence["name"], cls_switch=False)

    @staticmethod
    def _process_tags(tags: List[str], sequence_tags: str) -> List[Optional[str]]:
        """
        Return original tags / strip tags from sequence dataframe or return empty list()
        :param tags: tags given as function parameter
        :param sequence_tags: sequence dataframe tags
        :return:
        """
        if tags is not None:
            return tags
        elif sequence_tags:
            return [tag.strip() for tag in sequence_tags.split(',')]
        return list()

    def export_csv(self, *, g4hunter_analyse: Union[pd.DataFrame, pd.Series], out_path: str) -> None:
        """
        Export G4Hunter analyses result into csv files
        :param g4hunter_analyse: g4hunter analyse dataframe / series
        :param out_path: absolute path to output folder
        :return:
        """
        if isinstance(g4hunter_analyse, pd.Series):
            _id = g4hunter_analyse["id"]
            name = g4hunter_analyse["title"]
            file_path = os.path.join(out_path, f"{name}_{_id}.csv")

            with open(file_path, "w") as new_file:
                data = g4_export_csv(user=self.__user, id=_id, aggregate=True)
                new_file.write(data)
            print(f"file created -> {file_path}")
        # export multiple analyses
        else:
            for _, row in g4hunter_analyse.iterrows():
                _id = row["id"]
                name = row["title"]
                file_path = os.path.join(out_path, f"{name}_{_id}.csv")

                with open(file_path, "w") as new_file:
                    data = g4_export_csv(user=self.__user, id=_id, aggregate=True)
                    new_file.write(data)
                print(f"file created -> {file_path}")

    def delete(self, *, g4hunter_analyse: Union[pd.DataFrame, pd.Series]) -> None:
        """
        Delete G4Hunter analyse
        :param g4hunter_analyse: g4hunter analyse dataframe / series
        :return:
        """
        if isinstance(g4hunter_analyse, pd.DataFrame):
            for _, row in g4hunter_analyse.iterrows():
                _id = row["id"]
                if g4_delete_analyse(user=self.__user, id=_id):
                    print(f"G4hunter {_id} was deleted")
                    time.sleep(1)
                else:
                    print("G4hunter cannot be deleted")
        else:
            _id = g4hunter_analyse["id"]
            if g4_delete_analyse(user=self.__user, id=_id):
                print(f"G4hunter {_id} was deleted")
            else:
                print(f"G4hunter cannot be deleted")
