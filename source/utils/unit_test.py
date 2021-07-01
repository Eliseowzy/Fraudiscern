# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: 
@file: unit_test.py
@time: 7/1/2021
@version:
"""
import logger

_logger = logger.get_logger()


def spark_manager_test():
    spark_session = None
    _logger.info("Start spark_manager unit test.")
    import spark_manager
    try:
        _logger.info("Try to import spark_manager.")
        spark_session = spark_manager.get_spark_session()
    except ImportError:
        _logger.error("File to import 'spark_manager'.")
    if bool(spark_session):
        _logger.info("Unit test for spark_manager.get_spark_session() is pass.")


def hdfs_manager_test():
    hdfs_client = None
    _logger.info("Start hdfs_manager unit test.")
    import hdfs_manager
    try:
        hdfs_client = hdfs_manager.get_hdfs_client()
        _logger.info("Try to import hdfs_manager.")
    except ImportError:
        _logger.error("File to import 'hdfs_manager'.")
    if bool(hdfs_client):
        _logger.info("Unit test for hdfs_manager_test.get_hdfs_client() is pass.")


def data_loader_test(function='load_data_from_hdfs'):
    _logger.info("Start data_loader_test unit test.")
    data_set = None
    import data_loader
    if function == 'load_data_from_hdfs':
        try:
            source_path = "hdfs:///dataset/dataset_1/fraudTrain.csv"
            data_set = data_loader.load_data_from_hdfs(path=source_path)
        except IOError:
            _logger.error("Unit test for data_loader.loader_data_from_hdfs is NOT pass.")
        if bool(data_set):
            print(data_set.head(10))
            _logger.info("Unit test for data_loader.loader_data_from hdfs is pass.")


def main():
    # hdfs_manager_test()
    data_loader_test(function='load_data_from_hdfs')

    # spark_manager_test()
    exit(0)


if __name__ == '__main__':
    main()
