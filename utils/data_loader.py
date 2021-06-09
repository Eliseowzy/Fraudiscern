# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# Name: data_generator.py
# Developer:
# Date:
# Version:
# ******************************************************************************

import pandas as pd

import hdfs_manager
import data_generator as dg

_hdfs_client = hdfs_manager.get_hdfs_client()


def load_data_from_pkl(path):
    """
    Load pandas dataframe from source memory dump file path.
    :param path: Source memory dump file path.
    :return: dataset: pandas.DataFrame()
    """
    data_set = pd.read_pickle(path)
    return data_set


def load_data_to_pkl(data_set, path):
    """
    Load pandas dataframe to target memory dump file path.
    :param data_set: A pandas data frame.
    :param path: target memory dump file path
    :return: None
    """

    data_set.to_pickle(path)
    return None


def load_data_from_csv(path):
    """
    Load pandas dataframe from source csv file path.
    :param path: Source csv file path.
    :return: dataset: pandas.DataFrame()
    """

    data_set = pd.read_csv(path)
    return data_set


def load_data_to_csv(data_set, path):
    """
    Load pandas dataframe to source csv file path.
    :param data_set: A pandas data frame.
    :param path: Target csv file path.
    :return: None
    """
    data_set.to_csv(path)
    return None


def load_data_from_hdfs(path):
    """
    Load dataset from hdfs source path.
    :param path: HDFS source path.
    :return: dataset: pandas.DataFrame()
    """
    global _hdfs_client
    with _hdfs_client.read(path, 'utf-8') as fs:
        data_set = pd.read_csv(fs, index_col=0)
    return data_set


def load_data_to_hdfs(data_set, path):
    """
    Load dataset to hdfs target path.
    :param data_set: A pandas data frame.
    :param path: HDFS target path.
    :return: None.
    """
    global _hdfs_client
    with _hdfs_client.write(path, encoding='utf-8')as fs:
        data_set.to_csv(fs)
    return None
