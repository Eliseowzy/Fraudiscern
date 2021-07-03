from __future__ import division
import random
import pandas as pd
import sys
import datetime
from datetime import date
from random import randint
from faker import Faker

import profile_weights


def get_user_input():
    # convert date to datetime object
    global customers, pro, pro_fraud, pro_name, pro_name_fraud, startd, endd, m, file_path

    def convert_date(d):
        for char in ['/', '-', '_', ' ']:
            if char in d:
                d = d.split(char)
                try:
                    return date(int(d[2]), int(d[0]), int(d[1]))
                except:
                    error_msg(3)
        error_msg(3)

    # error handling for CL inputs
    def error_msg(n):
        if n == 1:
            print('Could not open customers file\n')
        elif n == 2:
            print('Could not open main config json file\n')
        else:
            print('Invalid date (MM-DD-YYYY)')
        output = 'ENTER:\n(1) Customers csv file\n'
        output += '(2) profile json file\n'
        output += '(3) Start date (MM-DD-YYYY)\n'
        output += '(4) End date (MM-DD-YYYY)\n'
        print(output)

    try:
        customers = pd.read_csv(sys.argv[1])
        # customers = pd.read_csv(".\data\customers_test.csv")

    except:
        error_msg(1)
    try:
        m = str(sys.argv[2])
        pro_name = m.split('profiles')[-1]
        pro_name = pro_name[1:]
        parse_index = m.index('profiles') + 9
        m_fraud = m[:parse_index] + 'fraud_' + m[parse_index:]

        pro = open(m, 'r').read()

        pro_fraud = open(m_fraud, 'r').read()

        pro_name_fraud = 'fraud_' + pro_name
        # fix for windows file paths


    except:
        error_msg(2)
    try:
        startd = convert_date(sys.argv[3])
        # startd = convert_date('01-01-2013')
    except:
        error_msg(3)
    try:
        endd = convert_date(sys.argv[4])
        # endd = convert_date('1-31-2013')
    except:
        error_msg(4)
    try:
        file_path = sys.argv[5]
    except:
        error_msg(5)

    return customers, pro, pro_fraud, pro_name, pro_name_fraud, startd, endd, m, file_path


def create_header(data):
    header = list(data.columns.values)
    header.extend(
        ['trans_num', 'trans_date', 'trans_time', 'unix_time', 'category', 'amt', 'is_fraud', 'merchant', 'merch_lat',
         'merch_long'])
    return header


class Customer:
    def __init__(self, customer, profile):
        self.customer = customer
        self.attrs = self.clean_row(self.customer)
        self.fraud_dates = []

    def print_trans(self, trans, is_fraud, fraud_dates):
        is_traveling = trans[1]
        travel_max = trans[2]
        data = pd.DataFrame()
        for t in trans[0]:
            ## Get transaction location details to generate appropriate merchant record
            cust_state = cust.attrs['state']
            groups = t.split('|')
            trans_cat = groups[4]
            merch_filtered = merch[merch['category'] == trans_cat]
            random_row = merch_filtered.loc[random.sample(list(merch_filtered.index), 1)]
            ##sw added list
            chosen_merchant = random_row.iloc[0]['merchant_name']

            cust_lat = cust.attrs['lat']
            cust_long = cust.attrs['long']

            if is_traveling:
                # hacky math.. assuming ~70 miles per 1 decimal degree of lat/long
                # sorry for being American, you're on your own for kilometers.
                rad = (float(travel_max) / 100) * 1.43

                # geo_coordinate() uses uniform distribution with lower = (center-rad), upper = (center+rad)
                merch_lat = fake.coordinate(center=float(cust_lat), radius=rad)
                merch_long = fake.coordinate(center=float(cust_long), radius=rad)
            else:
                # otherwise not traveling, so use 1 decimial degree (~70mile) radius around home address
                rad = 1
                merch_lat = fake.coordinate(center=float(cust_lat), radius=rad)
                merch_long = fake.coordinate(center=float(cust_long), radius=rad)
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
        return data

    def clean_row(self, row):
        # separate into a list of attrs
        # create a dict of name:value for each column
        attrs = {}
        for i in range(len(row)):
            attrs[headers[i]] = row[i]
        return attrs


# shell 示例 python datagen_transaction_new.py ".\data\customers.csv" ".\profiles\adults_2550_female_rural.json" 1-1-2012  1-31-2012  ".\data\adults_2550_female_rural.csv"
#                                           顾客csv文件存储地址     配置文件地址       开始时间 截止时间       csv文件存储地址
if __name__ == '__main__':
    # read user input into Inputs object
    # to prepare the user inputs
    # curr_profile is female_30_40_smaller_cities.json , for fraud as well as non fraud
    # profile_name is ./profiles/fraud_female_30_40_bigger_cities.json for fraud.
    customers, pro, pro_fraud, curr_profile, curr_fraud_profile, start, end, profile_name, file_path = get_user_input()
    # if curr_profile == "male_30_40_smaller_cities.json":
    #   inputCat = "travel"
    # elif curr_profile == "female_30_40_smaller_cities.json":
    #    inputCat = "pharmacy"
    # else:
    #    inputCat = "misc_net"

    # takes the customers headers and appends
    # transaction headers and returns/prints
    # if profile_name[11:][:6] == 'fraud_':
    # read merchant.csv used for transaction record
    #    merch = pd.read_csv('./data/merchants_fraud.csv' , sep='|')
    # else:
    #    merch = pd.read_csv('./data/merchants.csv', sep='|')

    headers = create_header(customers)
    # generate Faker object to calc merchant transaction locations
    fake = Faker()

    # for each customer, if the customer fits this profile
    # generate appropriate number of transactions
    data = pd.DataFrame()
    for index, row in customers.iterrows():
        profile = profile_weights.Profile(pro, start, end)
        cust = Customer(row, profile)
        if cust.attrs['profile'] == curr_profile:  # adults_2550_female_rural.json
            merch = pd.read_csv('data/merchants.csv', sep='|')
            is_fraud = 0

            fraud_flag = randint(0, 100)  # set fraud flag here, as we either gen real or fraud, not both for
            # the same day.
            fraud_dates = []

            # decide if we generate fraud or not
            if fraud_flag < 99:  # 11->25
                fraud_interval = randint(1, 1)  # 7->1
                inter_val = (end - start).days - 7
                # rand_interval is the random no of days to be added to start date
                rand_interval = randint(1, inter_val)
                # random start date is selected
                newstart = start + datetime.timedelta(days=rand_interval)
                # based on the fraud interval , random enddate is selected
                newend = newstart + datetime.timedelta(days=fraud_interval)
                # we assume that the fraud window can be between 1 to 7 days #7->1
                profile = profile_weights.Profile(pro_fraud, newstart, newend)
                cust = Customer(row, profile)
                merch = pd.read_csv('data/merchants.csv', sep='|')
                is_fraud = 1
                temp_tx_data = profile.sample_from(is_fraud)
                fraud_dates = temp_tx_data[3]
                transaction = cust.print_trans(temp_tx_data, is_fraud, fraud_dates)
                data = data.append(transaction)
                # parse_index = m.index('profiles/') + 9
                # m = m[:parse_index] +'fraud_' + m[parse_index:]

            # we're done with fraud (or didn't do it) but still need regular transactions
            # we pass through our previously selected fraud dates (if any) to filter them
            # out of regular transactions
            profile = profile_weights.Profile(pro, start, end)
            merch = pd.read_csv('data/merchants.csv', sep='|')
            is_fraud = 0
            temp_tx_data = profile.sample_from(is_fraud)
            transaction = cust.print_trans(temp_tx_data, is_fraud, fraud_dates)
            data = data.append(transaction)
    data.to_csv(file_path, index=False)
