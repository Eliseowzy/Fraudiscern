from __future__ import division

import datetime
import random
from datetime import date
from random import randint

import pandas as pd
from faker import Faker

from source.utils.data_generator_module import profile_weights


def get_user_input(customer_data_path="./data/customers.csv", profile_path="./profiles/adults_2550_female_rural.json",
                   start_date="1-1-2012", end_date="1-31-2012", file_path="./data/adults_2550_female_rural.csv"):
    # convert date to datetime object
    def convert_date(d):
        for char in ['/', '-', '_', ' ']:
            if char in d:
                d = d.split(char)
                return date(int(d[2]), int(d[0]), int(d[1]))

    customers = pd.read_csv(customer_data_path)
    # customers = pd.read_csv(".\data\customers_test.csv")

    m = str(profile_path)
    pro_name = m.split('profiles')[-1]
    pro_name = pro_name[1:]
    parse_index = m.index('profiles') + 9
    m_fraud = m[:parse_index] + 'fraud_' + m[parse_index:]
    pro = open(m, 'r').read()
    pro_fraud = open(m_fraud, 'r').read()
    pro_name_fraud = 'fraud_' + pro_name

    start_date_new = convert_date(start_date)
    # start_date = convert_date('01-01-2013')

    end_date_new = convert_date(end_date)
    # end_date = convert_date('1-31-2013')

    output_path = file_path

    return customers, pro, pro_fraud, pro_name, pro_name_fraud, start_date_new, end_date_new, m, output_path


def create_header(data):
    header = list(data.columns.values)
    header.extend(
        ['trans_num', 'trans_date', 'trans_time', 'unix_time', 'category', 'amt', 'is_fraud', 'merchant', 'merch_lat',
         'merch_long'])
    return header


class Transaction:
    def __init__(self, customer, headers):
        self.customer = customer
        self.headers = headers
        self.attributes = self.clean_row(self.customer)
        self.fraud_dates = []
        self.merch = pd.read_csv('/home/hduser/fraudiscern/source/utils/data_generator_module/data/merchants.csv',
                                 sep='|')
        self.fake = Faker()

    def generate_transaction_data(self, transaction, trans, is_fraud, fraud_dates):
        is_traveling = trans[1]
        travel_max = trans[2]
        transaction_data = pd.DataFrame()

        for t in trans[0]:
            # Get transaction location details to generate appropriate merchant record
            groups = t.split('|')
            trans_cat = groups[4]
            merch_filtered = self.merch[self.merch['category'] == trans_cat]
            random_row = merch_filtered.loc[random.sample(list(merch_filtered.index), 1)]
            chosen_merchant = random_row.iloc[0]['merchant_name']
            customer_lat = transaction.attributes['lat']
            customer_long = transaction.attributes['long']
            if is_traveling:
                rad = (float(travel_max) / 100) * 1.43

                merch_lat = self.fake.coordinate(center=float(customer_lat), radius=rad)
                merch_long = self.fake.coordinate(center=float(customer_long), radius=rad)
            else:

                rad = 1
                merch_lat = self.fake.coordinate(center=float(customer_lat), radius=rad)
                merch_long = self.fake.coordinate(center=float(customer_long), radius=rad)
            df1 = self.customer.to_frame()
            df2 = pd.DataFrame(df1.values.T, index=df1.columns, columns=df1.index)
            info = t.split("|")
            df2["trans_num"] = info[0]
            df2["trans_date"] = info[1]
            df2["trans_time"] = info[2]
            df2["unix_time"] = info[3]
            df2["category"] = info[4]
            df2["amt"] = info[5]
            df2["is_fraud"] = info[6]
            df2["merchant"] = chosen_merchant
            df2["merch_lat"] = merch_lat
            df2["merch_long"] = merch_long
            if is_fraud == 0 and groups[1] not in fraud_dates:
                transaction_data = transaction_data.append(df2)
            if is_fraud == 1:
                transaction_data = transaction_data.append(df2)
        # print(transaction_data)
        return transaction_data

    def clean_row(self, row):
        attributes = {}
        for i in range(len(row)):
            attributes[self.headers[i]] = row[i]
        return attributes


# shell 示例 python datagen_transaction_new.py ".\data\customers.csv" ".\profiles\adults_2550_female_rural.json"
# 1-1-2012  1-31-2012  ".\data\adults_2550_female_rural.csv"
"""
# shell每一项的含义
#"./data/customers.csv": 顾客csv文件存储地址     
#"./profiles/adults_2550_female_rural.json": 配置文件地址
# 1-1-2012: 开始时间
# 1-31-2012: 截止时间
# "./data/adults_2550_female_rural.csv":csv文件存储地址

"""


def helper(customer_data_path="./data/customers.csv", profile_path="./profiles/adults_2550_female_rural.json",
           start_date="1-1-2012", end_date="1-31-2012", file_path="./data/adults_2550_female_rural.csv"):
    customer_profiles, pro, pro_fraud, curr_profile, curr_fraud_profile, start, end, profile_name, file_path = get_user_input(
        customer_data_path, profile_path, start_date, end_date, file_path)
    headers = create_header(customer_profiles)
    transaction_data_set = pd.DataFrame()
    for index, row in customer_profiles.iterrows():
        # profile = profile_weights.Profile(pro, start, end)
        transaction = Transaction(row, headers)
        # print(transaction.attributes['profile'], "\t\t\t\t", curr_profile)
        # if transaction.attributes['profile'] == curr_profile:
        if True:
            fraud_flag = randint(0, 100)
            fraud_dates = []
            if fraud_flag < 99:
                fraud_interval = randint(1, 1)
                inter_val = (end - start).days - 7
                rand_interval = randint(1, inter_val)
                new_start = start + datetime.timedelta(days=rand_interval)
                new_end = new_start + datetime.timedelta(days=fraud_interval)
                profile = profile_weights.Profile(pro_fraud, new_start, new_end)
                transaction = Transaction(row, headers)
                is_fraud = 1
                temp_tx_data = profile.sample_from(is_fraud)
                fraud_dates = temp_tx_data[3]
                transaction_record = transaction.generate_transaction_data(transaction, temp_tx_data, is_fraud,
                                                                           fraud_dates)
                transaction_data_set = transaction_data_set.append(transaction_record)
                # print("transaction_record{}".format(transaction_record))
                # print("transaction_data_set{}".format(transaction_data_set))
            profile = profile_weights.Profile(pro, start, end)
            is_fraud = 0
            temp_tx_data = profile.sample_from(is_fraud)
            transaction_record = transaction.generate_transaction_data(transaction, temp_tx_data, is_fraud, fraud_dates)
            transaction_data_set = transaction_data_set.append(transaction_record)
    return transaction_data_set
