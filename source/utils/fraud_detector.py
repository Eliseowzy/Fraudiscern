# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Zhang Siyu, Wang Zhiyi
@file: fraud_detector.py
@time: 6/30/2021
@version: v1.0
"""

import json

import data_sampler
import kafka_manager
import model_persistence
import spark_manager

_spark_session = spark_manager.get_spark_session()
_spark_context = _spark_session.sparkContext
_kafka_consumer = kafka_manager.get_kafka_consumer()


def detect_one(model, record):
    record = _spark_session.createDataFrame(record)
    record = data_sampler.vectorize(record, 'is_fraud')
    detect_result = model.transcofrm(record)
    return detect_result


def detect(model_path='hdfs://10.244.35.208:9000/models/RandomForestModel/rf_1'):
    for message in _kafka_consumer:
        message_content = json.loads(message.value.decode())
        if message_content:
            message_topic = message.topic
            model = model_persistence.load_model_from_file(model_path)
            detect_result = detect_one(model, message_content)
            print(detect_result)


def main():
    detect()


if __name__ == '__main__':
    main()
