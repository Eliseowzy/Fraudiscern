from __future__ import division

import datetime
import random
import sys
from datetime import date
from random import randint

import pandas as pd
from faker import Faker

import profile_weights


def get_user_input(customer_data_path=".\data\customers.csv", profile_path=".\profiles\adults_2550_female_rural.json",
                   start_date="1-1-2012", end_date="1-31-2012"):
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

    start_date = convert_date(start_date)
    # start_date = convert_date('01-01-2013')

    end_date = convert_date(sys.argv[4])
    # end_date = convert_date('1-31-2013')

    file_path = sys.argv[5]

    return customers, pro, pro_fraud, pro_name, pro_name_fraud, start_date, end_date, m, file_path


def create_header(data):
    header = list(data.columns.values)
    header.extend(
        ['trans_num', 'trans_date', 'trans_time', 'unix_time', 'category', 'amt', 'is_fraud', 'merchant', 'merch_lat',
         'merch_long'])
    return header


class Transaction:
    def __init__(self, customer):
        self.customer = customer
        self.attrs = self.clean_row(self.customer)
        self.fraud_dates = []

    def print_trans(self, trans, is_fraud, fraud_dates, merch, fake):
        is_traveling = trans[1]
        travel_max = trans[2]
        data = pd.DataFrame()
        for t in trans[0]:
            # Get transaction location details to generate appropriate merchant record
            groups = t.split('|')
            trans_cat = groups[4]
            merch_filtered = merch[merch['category'] == trans_cat]
            random_row = merch_filtered.loc[random.sample(list(merch_filtered.index), 1)]

            chosen_merchant = random_row.iloc[0]['merchant_name']
            customer_lat = trans.attrs['lat']
            customer_long = trans.attrs['long']
            if is_traveling:
                rad = (float(travel_max) / 100) * 1.43

                merch_lat = fake.coordinate(center=float(customer_lat), radius=rad)
                merch_long = fake.coordinate(center=float(customer_long), radius=rad)
            else:

                rad = 1
                merch_lat = fake.coordinate(center=float(customer_lat), radius=rad)
                merch_long = fake.coordinate(center=float(customer_long), radius=rad)
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
                data = data.append(df2)
            if is_fraud == 1:
                data = data.append(df2)

    def clean_row(self, row):
        # separate into a list of attrs
        # create a dict of name:value for each column
        attrs = {}
        for i in range(len(row)):
            attrs[headers[i]] = row[i]
        return attrs


# shell 示例 python datagen_transaction_new.py ".\data\customers.csv" ".\profiles\adults_2550_female_rural.json"
# 1-1-2012  1-31-2012  ".\data\adults_2550_female_rural.csv"
"""
# shell每一项的含义
#".\data\customers.csv": 顾客csv文件存储地址     
#".\profiles\adults_2550_female_rural.json": 配置文件地址
# 1-1-2012: 开始时间
# 1-31-2012: 截止时间
# ".\data\adults_2550_female_rural.csv"csv: 文件存储地址

"""
if __name__ == '__main__':

    customers, pro, pro_fraud, curr_profile, curr_fraud_profile, start, end, profile_name, file_path = get_user_input()

    headers = create_header(customers)
    # generate Faker object to calc merchant transaction locations
    fake = Faker()

    # for each customer, if the customer fits this profile
    # generate appropriate number of transactions
    data = pd.DataFrame()
    for index, row in customers.iterrows():
        profile = profile_weights.Profile(pro, start, end)
        transaction = Transaction(row, profile)
        if transaction.attrs['profile'] == curr_profile:  # adults_2550_female_rural.json
            merch = pd.read_csv('data/merchants.csv', sep='|')
            is_fraud = 0

            fraud_flag = randint(0, 100)  # set fraud flag here, as we either gen real or fraud, not both for
            # the same day.
            fraud_dates = []

            if fraud_flag < 99:
                fraud_interval = randint(1, 1)
                inter_val = (end - start).days - 7

                rand_interval = randint(1, inter_val)

                newstart = start + datetime.timedelta(days=rand_interval)

                newend = newstart + datetime.timedelta(days=fraud_interval)

                profile = profile_weights.Profile(pro_fraud, newstart, newend)
                transaction = Transaction(row, profile)
                merch = pd.read_csv('data/merchants.csv', sep='|')
                is_fraud = 1
                temp_tx_data = profile.sample_from(is_fraud)
                fraud_dates = temp_tx_data[3]
                transaction = transaction.print_trans(temp_tx_data, is_fraud, fraud_dates)
                data = data.append(transaction)

            profile = profile_weights.Profile(pro, start, end)
            merch = pd.read_csv('data/merchants.csv', sep='|')
            is_fraud = 0
            temp_tx_data = profile.sample_from(is_fraud)
            transaction = transaction.print_trans(temp_tx_data, is_fraud, fraud_dates)
            data = data.append(transaction)
    data.to_csv(file_path, index=False)
