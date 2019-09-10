# singleton.py
# !/usr/bin/env python3
"""
Module with Singleton metaclass used in Api class.
"""


class Singleton(type):
    """Singleton metaclass"""

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
