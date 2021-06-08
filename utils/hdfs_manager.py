#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# Name: data_generator.py
# Developer:
# Data:
# Version:
# ******************************************************************************

from hdfs import Client

HDFS_HOST = "http://hduser:50070"
FILE_NAME = "/tmp/dataset/part-001"
COLUMN_NAMES = ['a1', 'a2', 'a3', 'target']


def get_hdfs_client():
    client = Client(HDFS_HOST)
    return client
