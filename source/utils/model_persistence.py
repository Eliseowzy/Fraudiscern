# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: logger.py
@time: 6/20/2021
@version: 1.0
"""

from pyspark.ml.classification import RandomForestClassifier

from spark_manager import get_spark_session

_spark_session = get_spark_session()


def load_model_from_file(path):
    """

    Reconstruct a models from a file persisted with models.dump.

    Args:
        cls:
        path (string):
            The source path stores a models.

    Returns:
        ModelObject:
            Model object.
    """
    model = RandomForestClassifier.load(path=path)
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
    # dump(model, path)
    model.save(path=path)
    return None
