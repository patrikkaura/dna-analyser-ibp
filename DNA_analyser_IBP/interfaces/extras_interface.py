# extras_interface.py
# !/usr/bin/env python3

import csv
import os
import requests
import pandas as pd
from typing import List
from .intersection import G4Result, Anotation
from ..utils import exception_handler, normalize_name, Logger, _multifasta_parser


class Extras:
    _ANOTATION_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&retmode=text&rettype=ft&id='

    _INTERSECTION_DATAFRAME_COLUMNS = [
        'FEATURE',
        '0-1.2 BEFORE', '0-1.2 IN', '0-1.2 AFTER',
        '1.2-1.4 BEFORE', '1.2-1.4 IN', '1.2-1.4 AFTER',
        '1.4-1.6 BEFORE', '1.4-1.6 IN', '1.4-1.6 AFTER',
        '1.6-1.8 BEFORE', '1.6-1.8 IN', '1.6-1.8 AFTER',
        '1.8-2.0 BEFORE', '1.8-2.0 IN', '1.8-2.0 AFTER',
        '2.0-inf BEFORE', '2.0-inf IN', '2.0-inf AFTER'
    ]

    @exception_handler
    def anotation_downloader(self, path: str, filename: str, ncbi_id: str) -> None:
        """
        Anotation downloader used to download anotation by NCBI ID

        Args:
            path (str): path where to store new anotation file
            filename (str): filename of new anotation file
            ncbi_id (str): ncbi id used for identication of anotation on remote server
        """
        filename = normalize_name(name=filename)  # normalize filename

        if os.path.isdir(path):  # only in valid folder
            ncbi_id = ncbi_id.strip()
            Logger.info(f'Anotation {ncbi_id} is being downloaded!')
            response = requests.get(f'{Extras._ANOTATION_URL}{ncbi_id}')

            if response.status_code == 200 and response.text.startswith('>'):
                file_path = f'{path}/{filename}.txt'
                with open(file_path, 'w') as file:
                    file.write(response.text)
                    Logger.info(f'Anotation file [{filename}.txt] is created!')
        else:
            Logger.error(f'Invalid anotation folder path!')

    @exception_handler
    def anotation_parser(self, path: str) -> pd.DataFrame:
        """
        Parse anotation file into [DataFrame]

        Args:
            path (str): anotation file system path

        Returns:
            pd.DataFrame: anotation Dataframe
        """
        feature_list = list()

        with open(path, 'r') as file:
            feature_backup = str()
            for index, row in enumerate(file):
                feature_row = row.split('\t')
                if len(feature_row) == 3:
                    feature_backup = feature_row[2]  # save feature for other areas
                    feature_list.append(self._anotaion_parse_row(row=feature_row))
                elif len(feature_row) == 2:
                    feature_row.append(feature_backup)  # append feature
                    feature_list.append(self._anotaion_parse_row(row=feature_row))
        return pd.DataFrame(data=feature_list, columns=['start', 'end', 'lenght', 'feature'])

    @exception_handler
    def _anotaion_parse_row(self, *, row: list) -> list:
        """
        Parse anotation file row

        Args:
            row (list): anotation file row

        Returns:
            list: list [feature start, feature stop, feature lenght, feature name]
        """
        start = int(row[0].replace('>', '').replace('<', '').replace('\n', ''))
        stop = int(row[1].replace('>', '').replace('<', '').replace('\n', ''))
        feature = row[2].replace('\n', '')

        if start < stop:
            return [start, stop, stop - start, feature]
        return [stop, start, start - stop, feature]

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
                sequence_name = normalize_name(name=sequence_name)
                with open(f'{out_path}/{sequence_name}.txt', 'w') as fasta:
                    fasta.write(f'>{sequence_name}\n')
                    fasta.write(sequence_nucleic)
                    Logger.info(f"File {path}/{sequence_name}.txt was created!")
        else:
            Logger.error("Output path doesn't exist!")

    @exception_handler
    def anotation_itersection(self, analyse: str, anotation: str) -> pd.DataFrame:
        """
        Create intersection dataframe for given G4Hunter analyse and parsed anotation file
        Args:
            analyse (str): path to g4hunter analyse result file
            anotation (str): path to parsed anotation file

        Returns:
            (pd.DataFrame): intersection result
        """
        anotation_list = Extras._create_anotation_list(anotation=anotation)
        analyse_list = Extras._create_g4hunter_list(analyse=analyse)
        results = list()
        for anotation in anotation_list:
            result = [0, 0, 0] * 6
            for analyse in analyse_list:
                group_id = analyse.get_group_id()
                # remove PQS which will never use again
                if (anotation.before - analyse.position) >= 100000:
                    analyse_list.remove(analyse)
                # if too far from analyse
                if analyse.position > anotation.after:
                    break
                # intersect
                else:
                    result[0 * group_id] += anotation.is_before(analyse)
                    result[1 * group_id] += anotation.is_in(analyse)
                    result[2 * group_id] += anotation.is_after(analyse)
            results.append([anotation.feature] + result)
        return pd.DataFrame(data=results, columns=Extras._INTERSECTION_DATAFRAME_COLUMNS)

    @staticmethod
    @exception_handler
    def _create_anotation_list(anotation: str) -> List[Anotation]:
        """
        Return list of Anotation objects

        Returns:
            (List[Anotation]): anotations
        """
        anotation_list = list()
        with open(anotation, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)
            for row in reader:
                anotation_list.append(Anotation(start=int(row[1]), end=int(row[2]), feature=row[4]))
        anotation_list = sorted(anotation_list, key=lambda a: a.start)
        return anotation_list

    @staticmethod
    @exception_handler
    def _create_g4hunter_list(analyse: str) -> List[G4Result]:
        """
        Return list of G4Result objects

        Returns:
            (List[G4Result]): G4Hunter results
        """
        analyse_list = list()
        with open(analyse, 'r') as file:
            reader = csv.reader(file, delimiter='\t')
            next(reader)
            for row in reader:
                analyse_list.append(G4Result(position=int(row[1]), length=int(row[2]), score=float(row[4])))
            return analyse_list
