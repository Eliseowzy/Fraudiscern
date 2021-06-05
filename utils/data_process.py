import pandas as pd

_data_set = pd.DataFrame()


def load_data_from_pkl(path):
    global _data_set
    _data_set = pd.read_pickle(path)


def load_data_from_csv(path):
    global _data_set
    _data_set = pd.read_csv(path)


def save_data_to_pkl(path):
    global _data_set
    _data_set.to_pickle(path)


def save_data_to_csv(path):
    global _data_set
    _data_set.to_csv(path)
