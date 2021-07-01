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
    _logger.info("Start spark manager unit test.")
    import spark_manager
    try:
        _logger.info("Try to import spark_manager.")
        spark_session = spark_manager.get_spark_session()
    except ImportError:
        # print("File to import 'spark_manager'")
        _logger.error("File to import 'spark_manager'.")


def hdfs_manager_test():
    _logger.info("Start hdfs manager unit test.")
    import hdfs_manager
    try:
        hdfs_client = hdfs_manager.get_hdfs_client()
        _logger.info("Try to import hdfs_manager.")
    except ImportError:
        _logger.error("File to import 'hdfs_manager'.")


def main():
    # hdfs_manager_test()

    spark_manager_test()
    exit(0)
    # print("Hello world")


if __name__ == '__main__':
    main()
