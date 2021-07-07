# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: logger.py
@time: 6/20/2021
@version: 1.0
"""


import os

from pyspark.ml.pipeline import PipelineModel

from spark_manager import get_spark_session

_spark_session = get_spark_session()
_spark_context = _spark_session.sparkContext


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
    # model = RandomForestClassificationModel.load(path=path)
    # model = RandomForestClassifier.load(path=path)
    # model = PipelineModel.load(path)

    model = PipelineModel.load(path)
    os.system('echo -e "\033[31m\033[1m{}\033[0m"'.format(str(model)))
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

    model.write().overwrite().save(path=path)
    return None
