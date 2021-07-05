# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: kafka_manager.py
@time: 7/4/2021
@version:
"""
import json

from kafka import KafkaConsumer
from kafka import KafkaProducer


def get_kafka_producer():
    # 实例化一个KafkaProducer示例，用于向Kafka投递消息
    producer = _create_kafka_producer()
    return producer


def _create_kafka_producer():
    kafka_producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                   bootstrap_servers=['spark-797d5ccdb-2d4wd:9092'])
    return kafka_producer


def get_kafka_consumer():
    """return a kafka consumer instance

    """

    consumer = _create_kafka_consumer()
    return consumer


def _create_kafka_consumer():
    kafka_consumer = KafkaConsumer('test_data', bootstrap_servers=['spark-797d5ccdb-2d4wd:9092'])
    return kafka_consumer
