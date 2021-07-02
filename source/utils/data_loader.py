# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: data_loader.py
@time: 6/20/2021
@version: 1.0
"""

import pandas as pd

import hdfs_manager
import spark_manager

_hdfs_client = hdfs_manager.get_hdfs_client()
_spark_session = spark_manager.get_spark_session()


def load_data_from_pkl(path):
    """load_data_from_pkl

    Load pandas dataframe from source memory dump file path.

    Args:
        path (string): Source memory dump file path.

    Returns:
         pyspark.sql.dataframe.DataFrame: data_set
    """

    data_set = pd.read_pickle(path)
    data_set = _spark_session.createDataFrame(data_set)
    return data_set


def load_data_to_pkl(data_set, path):
    """

    Load data set into dump file.

    Args:
        data_set (pandas.DataFrame): A pandas data frame.
        path (string): target memory dump file path

    Returns:
        NoneType: None
    """
    data_set.to_pickle(path)
    return None


def load_data_from_csv(path):
    """load_data_from_csv

    Load pandas dataframe from source csv file path.

    Args:
        path ():  Source csv file path.
    Returns:
        pyspark.sql.dataframe.DataFrame: data_set
    """
    data_set = pd.read_csv(path)
    data_set = _spark_session.createDataFrame(data_set)
    return data_set


def load_data_to_csv(data_set, path):
    """Load pandas dataframe to source csv file path.

    Load pandas dataframe to source csv file path.

    Args:
        data_set (pandas.DataFrame):  A pandas data frame.
        path (string): Target csv file path.

    Returns:
        NoneType: None
    """
    data_set.write.csv(path)
    return None


def load_data_from_hdfs(path):
    """

    Load data_set from hdfs source path.

    Args:
        path (string): HDFS source path.
    Returns:
        pyspark.sql.dataframe.DataFrame: data_set
    """

    _spark_context = _spark_session.sparkContext
    data_set = _spark_session.read.csv(path=path, inferSchema=True, sep=',', header=True)
    # print(data_set.columns)
    attributes = data_set.columns[1:]
    attributes.remove('zip')
    attributes.remove('unix_time')
    data_set = data_set.select(attributes)
    # print(data_set.head(2))
    return data_set


def load_data_to_hdfs(data_set, path):
    """

    Load data_set to hdfs target path.

    Args:
        data_set (pandas.DataFrame): A pandas data frame.
        path (string): HDFS target path.

    Returns:
        NoneType: None.
    """

    global _hdfs_client
    with _hdfs_client.write(path)as fs:
        data_set.to_csv(fs)
    return None
