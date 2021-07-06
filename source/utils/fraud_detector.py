# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Zhang Siyu, Wang Zhiyi
@file: fraud_detector.py
@time: 6/30/2021
@version: v1.0
"""

import json

from pyspark.sql.functions import col
from pyspark.sql.types import DoubleType

import kafka_manager
import model_persistence
import spark_manager

_spark_session = spark_manager.get_spark_session()
_spark_context = _spark_session.sparkContext


def _detect_one(model, record):
    """detect fraud for each record

    Args:
        model (PipelineModel): The trained model.
        record (Str): The content of each transaction record.

    Returns:
        [type]: [description]
    """
    record = _spark_session.read.json(_spark_context.parallelize([record]))

    for i in record.columns:
        record = record.withColumn(i, col(i).cast(DoubleType()))
    # record = data_sampler.vectorize(record, 'is_fraud')
    record = record.select("cc_num", "amt", "zip", "lat", "long", "city_pop", "unix_time", "merch_lat", "merch_long",
                           "is_fraud")
    detect_result = model.transform(record)
    detect_result = detect_result.toPandas().to_json()
    return detect_result


# model_path="hdfs://10.244.35.208:9000/models/RandomForestModel/rf_1"
def detect(model_path="hdfs:///models/RandomForestModel/rf_1"):
    """detect fraud

    Args:
        model_path (str, optional): the path of trained model stored in HDFS. Defaults to "hdfs://10.244.35.208:9000/models/RandomForestModel/random_forest_1".
    """
    _kafka_consumer = kafka_manager.get_kafka_consumer()
    for message in _kafka_consumer:
        message_content = json.loads(message.value.decode())
        print("Received message is: {}".format(message_content))
        if message_content:
            message_topic = message.topic
            model = model_persistence.load_model_from_file(model_path)
            detect_result = _detect_one(model, message_content)
            print(detect_result)


def main():
    detect()


if __name__ == '__main__':
    main()
