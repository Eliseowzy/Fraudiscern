# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: unit_test.py
@time: 7/4/2021
@version: 1.0
"""
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import warnings

import logger

warnings.filterwarnings('ignore')
_logger = logger.get_logger()


def spark_manager_test():
    """[summary]
    """
    spark_session = None
    _logger.info("Start spark_manager unit test.")
    try:
        _logger.info("Try to import spark_manager.")
        command = "spark-submit --master yarn spark_manager.py"
        os.system(command)
    except Exception:
        _logger.error("File to import 'spark_manager'.")
    if bool(spark_session):
        _logger.info("Unit test for spark_manager.get_spark_session() is pass.")


def hdfs_manager_test():
    """[summary]
    """
    hdfs_client = None
    _logger.info("Start hdfs_manager unit test.")
    import hdfs_manager
    try:
        hdfs_client = hdfs_manager.get_hdfs_client()
        _logger.info("Try to import hdfs_manager.")
    except Exception:
        _logger.error("File to import 'hdfs_manager'.")
    if bool(hdfs_client):
        _logger.info("Unit test for hdfs_manager_test.get_hdfs_client() is pass.")


def data_loader_test(function='load_data_from_hdfs'):
    """[summary]
    """
    _logger.info("Start data_loader_test unit test.")
    data_set = None
    import data_loader
    if function == 'load_data_from_hdfs':
        try:
            source_path = "hdfs://10.244.35.208:9000/dataset/dataset_1/fraudTest.csv"
            data_set = data_loader.load_data_from_hdfs(path=source_path)
        except Exception:
            _logger.error("Unit test for data_loader.{} is NOT pass.".format(function))
        if bool(data_set):
            print(data_set.head(5))
            _logger.info("Unit test for data_loader.{} hdfs is pass.".format(function))
    if function == 'load_data_to_csv':

        try:
            source_path = "hdfs://10.244.35.208:9000/dataset/dataset_1/fraudTest.csv"
            target_path = "hdfs://10.244.35.208:9000/dataset/dataset_1/fraud_test.csv"
            data_set = data_loader.load_data_from_hdfs(path=source_path)
            data_loader.load_data_to_csv(data_set, target_path)
            data_set = data_loader.load_data_from_hdfs(target_path)
        except Exception:
            _logger.error("Unit test for data_loader.{} is NOT pass.".format(function))
        if bool(data_set):
            print(data_set.head(1))


def model_persistence_test():
    """[summary]
    """
    _model_object = None
    # try:
    import model_persistence
    model_path = "hdfs://10.244.35.208:9000/models/RandomForestModel/random_forest_1"
    print("=================================")
    print("Start Model Persistence Test.")
    model = model_persistence.load_model_from_file(model_path)
    print(model)


def data_sampler_test():
    """[summary]
    """
    import data_loader
    import data_sampler
    new_data_set = None
    ratio_before, ratio_after = None, None
    try:
        data_set = data_loader.load_data_from_hdfs("hdfs://10.244.35.208:9000/dataset/dataset_1/fraudTest.csv")
        ratio_before = data_set.groupby('is_fraud').count().toPandas()

        new_data_set = data_sampler.smote(data_set=data_set, target='is_fraud')
        ratio_after = new_data_set.groupby('label').count().toPandas()

    except Exception:
        _logger.error("Unit for data_sampler_test is NOT pass.")
    if ratio_before is not None and ratio_after is not None and new_data_set is not None:
        _logger.info("Unit test for data_sampler is pass.")
        print(ratio_before)
        print(ratio_after)
        print(type(new_data_set))
        print(new_data_set.head(2))
    else:
        _logger.error("Unit test for data_sample is not pass for known reason.")


def classifier_test():
    """[summary]
    """
    from source.classifier import classifier
    import spark_manager
    spark_session = spark_manager.get_spark_session()

    classifier_instance = classifier()
    classifier_instance.set_data_set("hdfs://10.244.35.208:9000/dataset/dataset_1/fraudTest.csv")
    classifier_instance.train_model()
    classifier_instance.save_model()
    classifier_instance.predict()
    spark_session.stop()
    # validation module test
    classifier_instance.validate_model(validate_method='accuracy')
    classifier_instance.validate_model(validate_method='auc')
    classifier_instance.validate_model(validate_method='precision')
    classifier_instance.validate_model(validate_method='recall')
    classifier_instance.detect_fraud()


def generator_test(function_name):
    """[summary]
    """
    try:
        if function_name == "gen_customer":
            from data_generator import generate_customer_data
            _logger.info("Module: data_generator.generate_customer_data is imported successfully.")
            customer_set = generate_customer_data()
            print(customer_set)
        if function_name == "gen_transaction":
            from data_generator import generate_transaction_data
            import pandas as pd
            _logger.info("Module: data_generator.generate_transaction_data is imported successfully.")
            transaction_set = generate_transaction_data()
            print(transaction_set['last'])
            pd.set_option('display.max_columns', None)
            print(transaction_set.describe())
            print(transaction_set.groupby('is_fraud').count())
    except Exception:
        _logger.error("Unit for generator_test.{} is NOT pass.".format(function_name))


def kafka_test():
    try:
        import kafka_manager
        from data_generator import generate_transaction_data
        import time
        import json
        producer = kafka_manager.get_kafka_producer()
        transaction_data_set = generate_transaction_data()
        test_topic = 'test_data'
        for index, row in transaction_data_set.iterrows():
            # Send a piece of transaction every 0.1 second.
            data = row.to_json()
            time.sleep(0.1)
            producer.send(topic=test_topic, value=data)
            print("{} has been send".format(data))
        consumer = kafka_manager.get_kafka_consumer(topic=test_topic)
        for message in consumer:
            message_content = json.loads(message.value.decode())
            message_topic = message.topic
            print("{} is received".format(message_content))
    except Exception:
        _logger.error("Unit for kafka_test is NOT pass.")


def main_test():
    """Entry to Unit test
    """
    # spark_manager_test()
    # generator_test("gen_transaction")
    classifier_test()
    # model_persistence_test()
    # data_sampler_test()
    # data_loader_test(function='load_data_to_csv')
    # data_loader_test(function='load_data_from_hdfs')

    # hdfs_manager_test()
    exit(0)


if __name__ == '__main__':
    main_test()
