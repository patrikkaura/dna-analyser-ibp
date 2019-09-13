# statusbar.py
# !/usr/bin/env python3

import time
from tqdm import tqdm
from typing import Callable

from .callers import G4HunterAnalyse, g4_load_by_id, seq_load_by_id, User


def status_bar(user: User, func: Callable, name: str, cls_switch: bool) -> None:
    """
    TQDM status bar
    :param user: user for auth
    :param func: function decorated by statusbar
    :param name: statusbart name field
    :param cls_switch: True = SequenceModel, False = AnalyseModel
    :return:
    """
    # tqdm status bar
    with tqdm(
            desc=f"Sequence {name} uploading"
            if cls_switch
            else f"Analyse {name} processing",
            unit=" % uploaded" if cls_switch else " % processed",
            ascii=True,
    ) as pbar:
        pbar.update(50)  # update to 50 %
        obj = func().sequence if cls_switch else func().analyse  # exec given function

        while True:
            pbar.update(50 - pbar.n)  # withou it doesn't work don't know why
            if obj and cls_switch:
                if obj.length is not None:  # that means if finnished
                    pbar.update(50)  # complete to to 100 %
                    return None
                else:
                    obj = seq_load_by_id(user=user, id=obj.id)  # reload object
            if obj and not cls_switch:
                if obj.finished is not None:  # that means analyse finnished
                    pbar.update(50)  # complete to to 100 %
                    return None
                if isinstance(obj, G4HunterAnalyse):
                    obj = g4_load_by_id(user=user, id=obj.id)  # reload g4hunter object
            time.sleep(1)
