# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Su Junjie,Wang Zhiyi
@file: data_generator.py
@time: 7/03/2021
@version: 1.0
"""

import pandas as pd

from data_generator_module.datagen_customer_new import Customer


def generate_customer_data(customer_number=10, seed=4444,
                           profile_path="/home/hduser/fraudiscern/source/utils/data_generator_module/profiles"
                                        "/main_config.json",
                           file_path="/home/hduser/fraudiscern/source/utils/data_generator_module/data/customers.csv"):
    """Customer data generator
    Args:
        customer_number (int, optional): The number of customers. Defaults to 10.
        seed (int, optional): A random seed for faker. Defaults to 4444.
        profile_path (str, optional): Customer Profile path. Defaults to "./profiles/main_config.json".
        file_path (str, optional): Output path to store the dataset in csv format. Defaults to "./data/customers.csv".
    Returns: pandas.DataFrame():  The customer data set in pandas frame format. Specially, if customer_number==1,
    the generator just generates one customer data.
    """

    data = pd.DataFrame()
    for _ in range(customer_number):
        fake_customer_df = Customer(customer_profile_path=profile_path, seed=seed).to_pandas_dataframe()
        data = data.append(fake_customer_df)
    data.to_csv(file_path, index=False)
    return data


def transaction_data():
    raise NotImplementedError("这里需要实现交易生成功能")
