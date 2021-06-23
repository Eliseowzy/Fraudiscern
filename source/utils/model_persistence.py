# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: logger.py
@time: 6/20/2021
@version: 1.0
"""

from joblib import dump
from joblib import load


def load_model_from_file(path):
    """

    Reconstruct a models from a file persisted with models.dump.

    Args:
        path (string):
            The source path stores a models.

    Returns:
        ModelObject:
            Model object.
    """

    model = load(path)
    return model


def load_model_to_file(model, path):
    """

    Persist an models object into one file.

    Args:
        model (ModelObject):
            The model object.
        path (string):
            The target path stores a models.

    Returns:
        NoneType: None
    """
    dump(model, path)
    return None
