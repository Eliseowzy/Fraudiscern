# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi (Based on Antoni Baum (Yard1) <antoni.baum@protonmail.com>)
@file: model_persistence.py
@time: 6/20/2021
@version: 1.0
"""
from joblib import dump
from joblib import load


def load_model_from_file(path):
    """
    Reconstruct a models from a file persisted with models.dump.
    :param path: The source path stores a models.
    :return: model object
    """
    model = load(path)
    return model


def load_model_to_file(model, path):
    """
    Persist an models object into one file.
    :param model: The models object.
    :param path: The target path stores a models.
    :return: None
    """
    dump(model, path)
    return None
