#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# Name: data_generator.py
# Developer:
# Date:
# Version:
# ******************************************************************************

import pandas as pd

from utils import logger

_data_set = None
_model = None
logger = logger.get_logger()


def _set_dataset(dataset):
    global _data_set
    _data_set = dataset


def set_data(dataset, test_proportion=0.05):
    if type(pd.DataFrame()) != type(dataset):
        raise TypeError("Dataset should be pandas dataframe!")
    train_proportion = 1 - test_proportion
    data = dataset.sample(frac=train_proportion, random_state=786)
    test_set = dataset.drop(data.index)
    data.reset_index(inplace=True, drop=True)
    test_set.reset_index(inplace=True, drop=True)
    print('Data for Modeling: ' + str(data.shape))
    print('Unseen Data For Predictions ' + str(test_set.shape))
    logger.info("Data has been loaded successfully.")


def compare_models(mode_list=None):
    logger.info("Compare models is not implemented.")
    if mode_list is None:
        mode_list = []
