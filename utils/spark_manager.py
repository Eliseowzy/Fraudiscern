#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# Name: spark_manager.py
# Developer: Zhang Siyu
# Data: 13.06.2021
# Version: v1
# ******************************************************************************

from pyspark.sql import SparkSession
from pyspark import SparkConf
import time


def get_spark_session():
    try:
        assert bool(GLOBAL_SPARK)
        return GLOBAL_SPARK
    except:
        return create_spark_session()


def create_spark_session():
    """
    Get a new spark session.

    returns: _SPARK_SESSION
    """

    # 按照时分秒给spark session命名
    _cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _spark_appName = "{}_{}".format("app", str(_cur_time))
    _conf = SparkConf().setMaster("yarn").setAppName(_spark_appName)
    _spark_session = SparkSession \
        .builder \
        .config(conf=_conf) \
        .getOrCreate()
    return _spark_session


GLOBAL_SPARK = create_spark_session()
