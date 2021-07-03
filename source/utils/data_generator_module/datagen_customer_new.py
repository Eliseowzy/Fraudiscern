# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Su Junjie,Wang Zhiyi
@file: data_generator.py
@time: 7/03/2021
@version: 1.0
"""

import random
from datetime import date

import numpy as np
import pandas as pd
from faker import Faker

from source.utils.data_generator_module import main_config
from source.utils.data_generator_module import demographics

fake = Faker()


class Headers:
    """Store the headers and print to stdout to pipe into csv"""

    def __init__(self):
        header = ['ssn', 'cc_num', 'first', 'last', 'gender', 'street',
                  'city', 'state', 'zip', 'lat', 'long', 'city_pop',
                  'job', 'dob', 'acct_num', 'profile']
        self.headers = header

    def __str__(self):
        return str(self.headers)


class Customer:
    def __init__(self, customer_profile_path, seed):
        global fake
        fake = Faker(seed)
        self.ssn = fake.ssn()
        self.gender, self.dob = None, None
        self.generate_age_gender()
        self.first = self.get_first_name()
        self.last = fake.last_name()
        self.street = fake.street_address()
        self.addy = None
        self.get_random_location()
        self.job = fake.job()
        self.cc = fake.credit_card_number()
        self.email = fake.email()
        self.account = fake.random_number(digits=12)
        self.profile = self.find_profile(customer_profile_path)

    def get_first_name(self):
        if self.gender == 'M':
            return fake.first_name_male()
        else:
            return fake.first_name_female()

    def generate_age_gender(self):
        age_gender = demographics.make_age_gender_dict()
        a = np.random.random()
        c = []
        for b in age_gender.keys():
            if b > a:
                c.append(b)
        g_a = age_gender[min(c)]
        dob = fake.date_time_this_century()
        # adjust the randomized date to yield the correct age
        start_age = (date.today() - date(dob.year, dob.month, dob.day)).days / 365.
        dob_year = dob.year - int(g_a[1] - int(start_age))

        # since the year is adjusted, sometimes Feb 29th won't be a day
        # in the adjusted year
        self.gender, self.dob = g_a[0][0], date(dob_year, dob.month, dob.day)
        return self.gender, self.dob

    # find nearest city
    def get_random_location(self):
        cities = demographics.make_cities()
        self.addy = cities[min(cities, key=lambda x: abs(x - random.random()))]
        return self.addy

    def find_profile(self, profile_path):
        age = (date.today() - self.dob).days / 365.25
        city_pop = float(self.addy.split('|')[-1])
        # turn all profiles into dicts to work with
        all_profiles = main_config.MainConfig(profile_path).config
        match = []
        for pro in all_profiles:
            # -1 represents infinity
            if self.gender in all_profiles[pro]['gender'] and \
                    age >= all_profiles[pro]['age'][0] and \
                    (age < all_profiles[pro]['age'][1] or all_profiles[pro]['age'][1] == -1) and \
                    city_pop >= all_profiles[pro]['city_pop'][0] and \
                    (city_pop < all_profiles[pro]['city_pop'][1] or
                     all_profiles[pro]['city_pop'][1] == -1):
                match.append(pro)
        if not match:
            match.append('leftovers.json')

        # found overlap -- write to log file but continue
        if len(match) > 1:
            f = open('profile_overlap_warnings.log', 'a')
            output = ' '.join(match) + ': ' + self.gender + ' ' + \
                     str(age) + ' ' + str(city_pop) + '\n'
            f.write(output)
            f.close()
        return match[0]

    def to_pandas_dataframe(self):
        addy = self.addy.split("|")
        city = addy[0]
        state = addy[1]
        zip_code = addy[2]
        lat = addy[3]
        long = addy[4]
        city_pop = addy[5]
        customer_info = [[self.ssn, self.cc, self.first, self.last, self.gender,
                          self.street, city, state, zip_code, lat, long, city_pop, self.job, self.dob, self.account,
                          self.profile]]

        customer_df = pd.DataFrame(customer_info, columns=Headers().headers)
        return customer_df

# shell 命令 python datagen_customer_new.py 10 4444 ".\profiles\main_config.json" ". \data\customers.csv"
# customer_number顾客数量 seed_num随机种子值 main main_config.json地址  file_path csv文件存储地址
