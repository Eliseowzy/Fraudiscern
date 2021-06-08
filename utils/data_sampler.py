#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# Name: data_generator.py
# Developer:
# Data:
# Version:
# ******************************************************************************

import pandas as pd
import spark_manager

data_set = pd.DataFrame()
_spark = spark_manager.get_spark_session()


def _get_label_proportion(data_set, target='label'):
    data_set = _spark.createDataFrame(data_set)


