# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: hdfs_manager.py
@time: 6/21/2021
@version: 1.0
"""

from hdfs import InsecureClient


def get_hdfs_client():
    """

    Get an hdfs client (singleton).

    Returns:
        hdfs.client.InsecureClient: HDFS Client.
    """
    try:
        assert bool(GLOBAL_HDFS)
        return GLOBAL_HDFS
    except:
        return _create_hdfs_client()


def _create_hdfs_client():
    """Create and return an HDFS client.

    Returns:
        hdfs.client.InsecureClient: HDFS Client.
    """
    hdfs_client = InsecureClient("http://127.0.0.1:50070")
    return hdfs_client


GLOBAL_HDFS = _create_hdfs_client()
