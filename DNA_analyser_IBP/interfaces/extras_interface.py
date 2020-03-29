# extras_interface.py
# !/usr/bin/env python3

import csv
import os
import requests
import pandas as pd
from typing import List, Union
from ..intersection.annotation import (
    Annotation,
    get_annotation_labels,
    create_annotation_list,
)
from ..intersection.g4hunter import G4Result, create_g4hunter_list

from ..utils import (
    Logger,
    get_file_name,
    normalize_name,
    exception_handler,
    _multifasta_parser,
)


class Extras:
    _ANNOTATION_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&retmode=text&rettype=ft&id="

    _INTERSECTION_DATAFRAME_COLUMNS = [
        "FEATURE",
        "0-1.2 BEFORE",
        "0-1.2 IN",
        "0-1.2 AFTER",
        "1.2-1.4 BEFORE",
        "1.2-1.4 IN",
        "1.2-1.4 AFTER",
        "1.4-1.6 BEFORE",
        "1.4-1.6 IN",
        "1.4-1.6 AFTER",
        "1.6-1.8 BEFORE",
        "1.6-1.8 IN",
        "1.6-1.8 AFTER",
        "1.8-2.0 BEFORE",
        "1.8-2.0 IN",
        "1.8-2.0 AFTER",
        "2.0-inf BEFORE",
        "2.0-inf IN",
        "2.0-inf AFTER",
    ]

    @exception_handler
    def annotation_downloader(self, path: str, filename: str, ncbi_id: str) -> None:
        """
        Annotation downloader used to download annotation by NCBI ID

        Args:
            path (str): path where to store new annotation file
            filename (str): filename of new annotation file
            ncbi_id (str): ncbi id used for identication of annotation on remote server
        """
        filename: str = normalize_name(name=filename)  # normalize filename

        if os.path.isdir(path):  # only in valid folder
            ncbi_id: str = ncbi_id.strip()
            Logger.info(f"Annotation {ncbi_id} is being downloaded!")
            response = requests.get(f"{Extras._ANNOTATION_URL}{ncbi_id}")

            if 200 <= response.status_code <= 300 and response.text.startswith(">"):
                file_path: str = f"{path}/{filename}.txt"
                with open(file_path, "w") as file:
                    file.write(response.text)
                    Logger.info(f"Annotation file [{filename}.txt] is created!")
            else:
                Logger.error(f"Annotation file {filename} cannot be downloaded!")
        else:
            Logger.error(f"Invalid annotation folder path!")

    @exception_handler
    def annotation_parser(self, annotation_path: str, parsed_path: str) -> None:
        """
        Parse annotation file into [DataFrame]

        Args:
            annotation_path (str): annotation file system path
            parsed_path (str): parsed annotation file in CSV
        """
        feature_list: list = list()

        with open(annotation_path, "r") as file:
            feature_backup: str = str()

            for index, row in enumerate(file):
                feature_row: str = row.split("\t")
                if len(feature_row) == 3:
                    # save feature for other areas
                    feature_backup: str = feature_row[2]
                    feature_list.append(self._annotaion_parse_row(row=feature_row))
                elif len(feature_row) == 2:
                    feature_row.append(feature_backup)  # append feature
                    feature_list.append(self._annotaion_parse_row(row=feature_row))
        # get new outpath with new filename
        path: str = get_file_name(
            original_path=annotation_path, out_path=parsed_path, file_format="csv"
        )
        Logger.info(f"Parsed annotation file ${path}  saved! ")
        return pd.DataFrame(
            data=feature_list, columns=["start", "end", "lenght", "feature"]
        ).to_csv(path)

    @exception_handler
    def _annotaion_parse_row(self, *, row: list) -> list:
        """
        Parse annotation file row

        Args:
            row (list): annotation file row

        Returns:
            list: list [feature start, feature stop, feature lenght, feature name]
        """
        start: int = int(row[0].replace(">", "").replace("<", "").replace("\n", ""))
        stop: int = int(row[1].replace(">", "").replace("<", "").replace("\n", ""))
        feature: str = row[2].replace("\n", "")

        if start < stop:
            return [start, stop, stop - start, feature]
        return [stop, start, start - stop, feature]

    def annotation_overlay(
        self,
        *,
        analyse_file: str,
        annotation_file: str,
        area_size: int = 100,
        overlay_path: str = "",
    ) -> Union[pd.DataFrame, None]:
        """
        Create overlay dataframe for given G4Hunter analyse and parsed annotation file

        Args:
            analyse_file (str): path to g4hunter analyse result file
            annotation_file (str): path to parsed annotation file
            area_size (int): size of overlay region outside annotation [Default=100]
            overlay_path (str): overlay csv file path (if want to save to csv) [Default=""]

        Returns:
            (pd.DataFrame): intersection result
        """
        if 0 < area_size <= 1000:
            annotation_list: List[Annotation] = create_annotation_list(
                annotation=annotation_file, area_size=area_size
            )
            analyse_list: List[G4Result] = create_g4hunter_list(analyse=analyse_file)

            labels: List[str] = get_annotation_labels(annotation_list=annotation_list)
            result: list = [[label] + [0, 0, 0] * 6 for label in labels]

            for annotation in annotation_list:
                for analyse in analyse_list:
                    group_id: int = analyse.get_group_id()
                    # remove PQS which will never use again (optimization)
                    if (annotation.before - analyse.position) >= 100000:
                        analyse_list.remove(analyse)
                    # if too far from analyse
                    if analyse.position > annotation.after:
                        break
                    # overlay
                    else:
                        label_index: int = labels.index(annotation.feature)
                        result[label_index][0 * group_id + 1] += annotation.is_before(
                            analyse
                        )
                        result[label_index][1 * group_id + 1] += annotation.is_in(
                            analyse
                        )
                        result[label_index][2 * group_id + 1] += annotation.is_after(
                            analyse
                        )
            # get outpath for overlay file
            if overlay_path:
                path: str = get_file_name(
                    original_path=annotation_file, out_path=overlay_path, file_format="csv"
                )
                pd.DataFrame(
                    data=result, columns=Extras._INTERSECTION_DATAFRAME_COLUMNS
                ).to_csv(path)
                Logger.info(f"Overlay analysis {path} save!")
                return None
            return pd.DataFrame(
                data=result, columns=Extras._INTERSECTION_DATAFRAME_COLUMNS
            )
        else:
            Logger.error("Overlay area must be in interval (0,1000>!")

    @exception_handler
    def multifasta_to_fasta(self, *, path: str, out_path: str) -> None:
        """
        Split one MultiFASTA file into multiple FASTA files

        Args:
            path (str): absolute system path into folder with MultiFASTA
            out_path (str): absolute system path into output folder with FASTAs
        """
        if os.path.exists(out_path):
            for sequence_name, sequence_nucleic in _multifasta_parser(path=path):
                sequence_name: str = normalize_name(name=sequence_name)

                with open(f"{out_path}/{sequence_name}.txt", "w") as fasta:
                    fasta.write(f">{sequence_name}\n")
                    fasta.write(sequence_nucleic)
                    Logger.info(f"File {path}/{sequence_name}.txt was created!")
        else:
            Logger.error("Output path doesn't exist!")
