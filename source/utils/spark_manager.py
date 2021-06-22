# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: spark_manager.py
@time: 6/20/2021
@version: 1.0
"""

from pyspark.sql import SparkSession
from pyspark import SparkConf
import time


def get_spark_session():
    """
    Get a spark session, if not exists call _crate_spark_session().
    :return:
    """
    try:
        assert bool(GLOBAL_SPARK)
        return GLOBAL_SPARK
    except:
        return _crate_spark_session()


def _crate_spark_session():
    """
    Create a spark session (singleton)
    :return:
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


GLOBAL_SPARK = _crate_spark_session()
