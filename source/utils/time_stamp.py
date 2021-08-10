# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: 
@file: time_stamp.py
@time: 7/13/2021
@version: 1.0
"""
import time

import dateutil.parser


def get_timestamp(time_format="%Y-%m-%d %H:%M:%S"):
    if time_format == "%Y-%m-%d %H:%M:%S":
        # add detect timestamp
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp


def get_timestamp_gap(time_format="%Y-%m-%d %H:%M:%S", start_time=None, end_time=None):
    if time_format == "%Y-%m-%d %H:%M:%S":
        time_detect = dateutil.parser.parse(end_time)
        time_send = dateutil.parser.parse(start_time)
        gap = (time_detect - time_send).total_seconds()
        return gap
    else:
        return None
