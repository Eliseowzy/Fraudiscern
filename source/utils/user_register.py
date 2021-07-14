# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author:
@file: user_register.py
@time: 7/15/2021
@version:
"""
import csv
import hashlib
import os
import random

import pandas as pd


def get_authentication_code(code_length):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(code_length):
        salt += random.choice(H)
    return salt


def get_hash_sha1(message):
    sha1 = hashlib.sha1()
    sha1.update(message.encode('utf-8'))
    return str(sha1.hexdigest())


def add_user(user_dict):
    path = "users.csv"
    if not os.path.exists("users.csv"):
        with open(path, 'wb') as f:
            csv_write = csv.writer(f)
            csv_head = ["username", "mail", "password"]
            csv_write.writerow(csv_head)
        with open(path, 'a+') as f:
            csv_write = csv.writer(f)
            data_row = [get_hash_sha1(str(user_dict["user_name"])), get_hash_sha1(str(user_dict["mail"])),
                        get_hash_sha1(str(user_dict["password2"]))]
            csv_write.writerow(data_row)
    else:
        if _check_user(str(user_dict["user_name"])):
            with open(path, 'a+') as f:
                csv_write = csv.writer(f)
                data_row = [get_hash_sha1(str(user_dict["user_name"])), get_hash_sha1(str(user_dict["mail"])),
                            get_hash_sha1(str(user_dict["password2"]))]
                csv_write.writerow(data_row)
                return True
        else:
            return False


def _check_user(user_name):
    df = pd.read_csv("users.csv")
    for row in df.iterrows():
        if user_name ^ row[0]:
            continue
        else:
            return False
    return True


print(get_authentication_code(6))
