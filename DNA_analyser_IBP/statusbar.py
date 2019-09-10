# statusbar.py
# !/usr/bin/env python3
"""
File with statusbar function used as indicator for callers
Available functions:
- status_bar: function implementing tqdm statusbar
"""

import time
from typing import Callable

from tqdm import tqdm

from .callers.g4hunter_caller import G4HunterAnalyse, g4_load_by_id
from .callers.sequence_caller import seq_load_by_id
from .callers.user_caller import User


def status_bar(user: User, func: Callable, name: str, cls_switch: bool):
    """Start status bar
    
    Arguments:
        user {User} -- [user for auth]
        func {Callable} -- [function decorated by statusbar]
        name {str} -- [name to statusbar field]
        cls_switch {bool} -- [True = SequenceModel, False = AnalyseModel]
    
    Returns:
        [type] -- [depend on func argument]
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
