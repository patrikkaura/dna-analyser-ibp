# g4hunter_interface.py
# !/usr/bin/env python3
"""Library with G4hunter interface object
Available classes:
G4Hunter - interface for interaction with g4hunter api
"""

import time
import os
import matplotlib.pyplot as plt
import pandas as pd

from .analyse_interface import AnalyseInterface
from ..statusbar import status_bar

from typing import List, Union
from ..callers.user_caller import User

from ..callers.g4hunter_caller import (
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

    def load_all(self, filter_tag: List[str] = None) -> pd.DataFrame:
        """Return all or filtered g4hunter analyses in dataframe
        
        Keyword Arguments:
            filter_tag {List[str]} -- [tags for analyse filtering] (default: {None})
        
        Returns:
            pd.DataFrame -- [dataframe with g4hunter analyses]
        """

        g4 = [g4 for g4 in g4_load_all(user=self.__user, filter_tag=filter_tag)]
        data = pd.concat([g.get_dataframe() for g in g4], ignore_index=True)
        
        return data

    def load_by_id(self, id: str) -> pd.DataFrame:
        """Return g4hunter analyses in dataframe
        
        Arguments:
            id {str} -- [g4hunter analyse id]
        
        Returns:
            pd.DataFrame -- [dataframe with g4hunter analyses]
        """

        g4 = g4_load_by_id(user=self.__user, id=id)
        
        return g4.get_dataframe()

    def load_results(self, g4hunter_analyse: pd.Series) -> pd.DataFrame:
        """Return g4hunter analyses results in dataframe
        
        Arguments:
            g4hunter_analyse {pd.Series} -- [g4hunter analyse series]
        
        Returns:
            pd.DataFrame -- [dataframe with g4hunter results]
        """

        if isinstance(g4hunter_analyse, pd.Series):
            return g4_load_result(user=self.__user, id=g4hunter_analyse["id"])
        else:
            raise ("You have to insert pd.Series")

    def load_heatmap(
        self,
        g4hunter_analyse: pd.Series,
        segment_count: int = 31,
        coverage: bool = False,
    ):
        """Return seaborn graph with heatmap
        
        Arguments:
            g4hunter_analyse {pd.Series} -- [g4hunter analyse series]
        
        Keyword Arguments:
            segment_count {int} -- [number of heatmap segments] (default: {31})
            coverage {bool} -- [True = coverage heatmap False = count heatmap] (default: {False})
        """

        if isinstance(g4hunter_analyse, pd.Series):
            data = g4_load_heatmap(
                user=self.__user, id=g4hunter_analyse["id"], segment_count=segment_count
            )

            ax = data[["coverage" if coverage else "count"]].plot(
                kind="bar", figsize=(14, 8), legend=True, fontsize=12
            )
            ax.set_xlabel("segments", fontsize=12)
            ax.set_ylabel("coverage [%/100]" if coverage else "count [-]", fontsize=12)
            
            plt.grid(color="k", linestyle="-", linewidth=0.1)
            plt.show()
        else:
            raise ("You have to insert pd.Series")

    def analyse_creator(
        self,
        sequence: Union[pd.DataFrame, pd.Series],
        tags: List[str],
        threshold: float,
        window_size: int,
    ):
        """Create G4hunter analyse
        
        Arguments:
            sequence {Union[pd.DataFrame, pd.Series]} -- [sequence/s to analyse]
            tags {List[str]} -- [tags for analyse filtering]
            threshold {float} -- [g4hunter threshold recommended 1.2]
            window_size {int} -- [g4hunter window size recommended 25]
        """

        # start g4hunter analyse factory
        if isinstance(sequence, pd.DataFrame):
            for _, row in sequence.iterrows():
                status_bar(
                    user=self.__user,
                    func=lambda: G4HunterAnalyseFactory(
                        user=self.__user,
                        id=row["id"],
                        tags=tags,
                        threshold=threshold,
                        window_size=window_size,
                    ),
                    name=row["name"],
                    cls_switch=False,
                )
        else:
            status_bar(
                user=self.__user,
                func=lambda: G4HunterAnalyseFactory(
                    user=self.__user,
                    id=sequence["id"],
                    tags=tags,
                    threshold=threshold,
                    window_size=window_size,
                ),
                name=sequence["name"],
                cls_switch=False,
            )

    def export_csv(
        self, g4hunter_analyse: Union[pd.DataFrame, pd.Series], out_path: str
    ):
        """[summary]
        
        Arguments:
            g4hunter_analyse {Union[pd.DataFrame, pd.Series]} -- [g4hunter analyse dataframe / series]
            out_path {str} -- [absolute path to output folder]
        """

        if isinstance(g4hunter_analyse, pd.Series):
            _id = g4hunter_analyse["id"]
            name = g4hunter_analyse["title"]
            file_path = os.path.join(out_path, f"{name}_{_id}.csv")

            with open(file_path, "w") as new_file:
                data = g4_export_csv(user=self.__user, id=_id)
                new_file.write(data)
            print(f"file created -> {file_path}")
        # export multiple analyses
        else:
            for _, row in g4hunter_analyse.iterrows():
                _id = row["id"]
                name = row["title"]
                file_path = os.path.join(out_path, f"{name}_{_id}.csv")

                with open(file_path, "w") as new_file:
                    data = g4_export_csv(user=self.__user, id=_id)
                    new_file.write(data)
                print(f"file created -> {file_path}")

    def delete(self, g4hunter_analyse: Union[pd.DataFrame, pd.Series]):
        """Delete g4hunter analyse
        
        Arguments:
            g4hunter_pandas {Union[pd.DataFrame, pd.Series]} -- [g4hunter analyse dataframe / series]
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
