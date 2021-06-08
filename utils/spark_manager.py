#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# Name: data_generator.py
# Developer:
# Data:
# Version:
# ******************************************************************************

from pyspark.sql import SparkSession

_SPARK_SESSION = None


def get_spark_session():
    global _SPARK_SESSION
    _SPARK_SESSION = SparkSession \
        .builder \
        .appName("fraud_dataset_loader") \
        .getOrCreate()
    return _SPARK_SESSION
