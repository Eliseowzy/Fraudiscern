# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: hdfs_manager.py
@time: 6/21/2021
@version: 1.0
"""

import hdfs
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


def create_dir(hdfs_root="dataset/", folder_name="user_123"):
    dir_name = hdfs_root + folder_name
    try:
        GLOBAL_HDFS.makedirs(dir_name)
    except hdfs.HdfsError:
        return "Root folder: {} not exits.".format(hdfs_root)
    return "{} created successfully.".format(folder_name)


def create_file(hdfs_path, data_set=None, overwrite=False, permission=None, block_size=None, replication=None,
                buffer_size=None,
                append=False, encoding='utf-8'):
    try:
        GLOBAL_HDFS.write(hdfs_path, data=data_set, overwrite=overwrite, permission=permission, blocksize=block_size,
                          replication=replication,
                          buffersize=buffer_size,
                          append=append, encoding=encoding)
    except hdfs.HdfsError:
        return "File: {} already exists.".format(hdfs_path)


def synchronize_file(hdfs_path, local_path, n_thread=3):
    try:
        GLOBAL_HDFS.upload(hdfs_path, local_path, n_threads=3)
    except hdfs.HdfsError:
        return "File {} already exists!".format(hdfs_path)


def get_file_names(path):
    file_list = GLOBAL_HDFS.list(hdfs_path=path)
    return file_list


GLOBAL_HDFS = _create_hdfs_client()
