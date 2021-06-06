import pandas as pd

import hdfs_manager
import data_generator as dg

_data_set = pd.DataFrame()
_hdfs_client = hdfs_manager.get_hdfs_client()


def load_data_from_pkl(path):
    global _data_set
    _data_set = pd.read_pickle(path)


def load_data_to_pkl(path):
    global _data_set
    _data_set.to_pickle(path)


def load_data_from_csv(path):
    global _data_set
    _data_set = pd.read_csv(path)


def load_data_to_csv(path):
    global _data_set
    _data_set.to_csv(path)


def load_data_from_hdfs():
    """
    Function: Load a dataframe from hdfs
    :return: pandas.Dataframe()
    """


def get_dataset():
    global _data_set
    return _data_set
