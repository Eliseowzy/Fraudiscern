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
from data_generator_module.datagen_transaction_new import helper


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


def generate_transaction_data(
        customer_data_path="/home/hduser/fraudiscern/source/utils/data_generator_module/data/customers.csv",
        profile_path="/home/hduser/fraudiscern/source/utils/data_generator_module/profiles/adults_2550_female_rural"
                     ".json",
        start_date="1-1-2012", end_date="1-31-2012",
        file_path="/home/hduser/fraudiscern/source/utils/data_generator_module/data/adults_2550_female_rural.csv"):
    """Generate transaction data.

    Args:
        customer_data_path (str, optional): The profile of consumer. Defaults to "/home/hduser/fraudiscern/source/utils/data_generator_module/data/customers.csv".
        profile_path (str, optional): The profile of merchant, location etc.. Defaults to "/home/hduser/fraudiscern/source/utils/data_generator_module/profiles/adults_2550_female_rural"".json".
        start_date (str, optional): The start date of the data set. Defaults to "1-1-2012".
        end_date (str, optional): [description]. Defaults to "1-31-2012".
        file_path (str, optional): [description]. Defaults to "/home/hduser/fraudiscern/source/utils/data_generator_module/data/adults_2550_female_rural.csv".

    Returns:
        pandas.DataFrame: The transaction data set.
    """
    transaction_data_set = helper(customer_data_path=customer_data_path, profile_path=profile_path,
                                  start_date=start_date, end_date=end_date, file_path=file_path)
    columns = ['cc_num', 'amt', 'zip', 'lat', 'long', 'city_pop', 'unix_time', 'merch_lat', 'merch_long', 'is_fraud']
    transaction_data_set = transaction_data_set[columns]
    transaction_data_set.to_csv(file_path, index=False)
    return transaction_data_set
    # raise NotImplementedError("这里需要实现交易生成功能")
