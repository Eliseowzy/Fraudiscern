# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: hdfs_manager.py
@time: 6/20/2021
@version: 1.0
"""

from hdfs import InsecureClient


def get_hdfs_client():
    hdfs_client = InsecureClient("http://127.0.0.1:50070")
    return hdfs_client
