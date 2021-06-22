#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# Name: data_generator.py
# Developer: Wang Zhiyi
# Date: 2021-06-21
# Version: 1.0
# ******************************************************************************

from hdfs import InsecureClient


def get_hdfs_client():
    hdfs_client = InsecureClient("http://127.0.0.1:50070")
    return hdfs_client
