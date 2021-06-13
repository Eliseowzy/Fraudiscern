#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# Name: data_generator.py
# Developer:
# Data:
# Version:
# ******************************************************************************

from pyspark.sql import SparkSession
from pyspark import SparkConf

_SPARK_SESSION = None


def get_spark_session(appName):
    global _SPARK_SESSION
    conf = SparkConf().setMaster("yarn").setAppName(appName)
    _SPARK_SESSION = SparkSession \
        .builder \
        .config(conf=conf) \
        .getOrCreate()
    return _SPARK_SESSION
