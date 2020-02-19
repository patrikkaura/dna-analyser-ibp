# extras_interface.py
# !/usr/bin/env python3

import os
import requests
import pandas as pd
from ..utils import exception_handler, normalize_name, Logger, _multifasta_parser


class Extras:
    ANOTATION_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&retmode=text&rettype=ft&id='

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
            response = requests.get(f'{Extras.ANOTATION_URL}{ncbi_id}')

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
