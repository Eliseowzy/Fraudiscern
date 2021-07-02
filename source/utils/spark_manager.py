# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Zhang Siyu, Wang Zhiyi
@file: spark_manager.py
@time: 6/21/2021
@version: 1.1
"""

import time

from pyspark import SparkConf
from pyspark.sql import SparkSession


def get_spark_session():
    """Get a spark session, if not exists call _crate_spark_session().

    Returns:
        SparkSession: GLOBAL_SPARK
    """
    try:
        assert bool(GLOBAL_SPARK)
        return GLOBAL_SPARK
    except:
        return _crate_spark_session()


def _crate_spark_session():
    """Create a spark session (singleton)

    Returns:
        SparkSession: _spark_session
    """

    # 按照时分秒给spark session命名
    _cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _spark_appName = "{}_{}".format("spark_app", str(_cur_time))
    # _conf = SparkConf().setMaster("yarn").setAppName(_spark_appName)
    _conf = SparkConf().\
        setAppName(_spark_appName).\
        set("spark.executor.memory", '8g').\
        set("spark.driver.memory", '8g')

    _spark_session = SparkSession \
        .builder \
        .config(conf=_conf) \
        .getOrCreate()
    return _spark_session


GLOBAL_SPARK = _crate_spark_session()
