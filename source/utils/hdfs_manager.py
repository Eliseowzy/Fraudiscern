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
    """Create a folder on the HDFS.

    Args:
        hdfs_root (str, optional): The root dictionary for users. Defaults to "dataset/".
        folder_name (str, optional): The folder name. Defaults to "user_123".

    Returns:
        str: Folder already exists. Folder created successfully.
    """
    dir_name = hdfs_root + folder_name
    try:
        GLOBAL_HDFS.makedirs(dir_name)
    except hdfs.HdfsError:
        return "Root folder: {} not exits.".format(hdfs_root)
    return "{} created successfully.".format(folder_name)


def create_file(hdfs_path, data_set=None, overwrite=False, permission=None, block_size=None, replication=None,
                buffer_size=None,
                append=False, encoding='utf-8'):
    """Create a file on the hdfs.

    Args:
        hdfs_path (str): [description]
        data_set (), optional): [description]. Defaults to None.
        overwrite (bool, optional): [description]. Defaults to False.
        permission ([type], optional): [description]. Defaults to None.
        block_size ([type], optional): [description]. Defaults to None.
        replication ([type], optional): [description]. Defaults to None.
        buffer_size ([type], optional): [description]. Defaults to None.
        append (bool, optional): [description]. Defaults to False.
        encoding (str, optional): [description]. Defaults to 'utf-8'.

    Returns:
        [type]: [description]
    """
    try:
        GLOBAL_HDFS.write(hdfs_path, data=data_set, overwrite=overwrite, permission=permission, blocksize=block_size,
                          replication=replication,
                          buffersize=buffer_size,
                          append=append, encoding=encoding)
    except hdfs.HdfsError:
        return "File: {} already exists.".format(hdfs_path)


def synchronize_file(hdfs_path, local_path, n_thread=3):
    """Synchromize a local file on HDFS.

    Args:
        hdfs_path (str): 
        local_path (str): [description]
        n_thread (int, optional): [description]. Defaults to 3.

    Returns:
        [type]: [description]
    """
    try:
        GLOBAL_HDFS.upload(hdfs_path, local_path, n_threads=n_thread)
    except hdfs.HdfsError:
        return "File {} already exists!".format(hdfs_path)


def get_file_names(path):
    """Get the files as a list under a path.

    Args:
        path (str): Target folder path.

    Returns:
        list: A file list under the folder.
    """
    file_list = GLOBAL_HDFS.list(hdfs_path=path)
    return file_list


GLOBAL_HDFS = _create_hdfs_client()
