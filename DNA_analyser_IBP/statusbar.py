# statusbar.py

import time
from typing import Callable

from tqdm import tqdm

from DNA_analyser_IBP.models import Batch
from DNA_analyser_IBP.ports import Ports
from DNA_analyser_IBP.type import Types
from DNA_analyser_IBP.utils import Logger


def status_bar(ports: Ports, func: Callable, name: str, type: str) -> None:
    """
    TQDM status bar

    Args:
        ports (Ports): ports
        func (Callable): function decorated by statusbar
        name (str): name field
        type (bool): True = SequenceModel, False = AnalyseModel
    """

    description_text = str()
    if type in [Types.G4HUNTER, Types.RLOOPR, Types.PALINDROME]:
        description_text = f"Analysing sequence -> {name}"
    elif type == Types.SEQUENCE:
        description_text = f"Uploading sequence -> {name}"

    with tqdm(
        desc=description_text,
        unit=" %",
        ascii=True,
    ) as statusbar:
        statusbar.update(50)  # update to 50 %

        function_result = func()  # exec given function

        while True:
            statusbar.update(50 - statusbar.n)  # without it doesn't work don't know why

            if type == Types.SEQUENCE:
                batch: Batch = ports.batch.get_batch_status(
                    id=function_result.id, type=type
                )
                if batch.is_finished():  # that means if finished
                    statusbar.update(50)  # complete to to 100 %
                    return None
                elif batch.is_failed():
                    Logger.error(f"Uploading sequence {function_result.name} failed!")
                    return None

            elif type in [Types.G4HUNTER, Types.RLOOPR, Types.PALINDROME]:
                batch: Batch = ports.batch.get_batch_status(
                    id=function_result.id, type=type
                )
                if batch.is_finished():  # that means analyse finished
                    statusbar.update(50)  # complete to to 100 %
                    return None
                elif batch.is_failed():
                    Logger.error(f"Analyse {function_result.name} failed!")
                    return None
            time.sleep(0.5)
