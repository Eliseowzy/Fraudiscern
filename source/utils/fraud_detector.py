# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Zhang Siyu, Wang Zhiyi
@file: fraud_detector.py
@time: 6/30/2021
@version: v1.0
"""

from pyspark.sql import Row
from pyspark.streaming import StreamingContext

import kafka_consumer
import model_persistence
import spark_manager

_spark_session = spark_manager.get_spark_session()
_spark_context = _spark_session.sparkContext


def detect_one(record, spark, model):
    """Detect a piece of record based on a model in spark streaming.

    Args:
        record (string): A piece of record.
        spark (spark session): A spark session.
        model (pkl): A pickle model file object.
    """
    try:
        record = record.filter(lambda x: len(x) > 0)

        rowRdd = record.map(lambda w: Row(transaction=w))

        recordsDataFrame = spark.createDataFrame(rowRdd)

        model.transform(recordsDataFrame)
    except:
        print('No data')


def detect(model_path='hdfs:///models/RandomForestModel/rf_1', topic=None):
    """Use the model in model_path to detect.

    Args:
        model_path (str, optional): The location of a model. Defaults to 'hdfs:///models/RandomForestModel/rf_1'.
        topic ([type], optional): The topic of kafka consumer. Defaults to None.
    """
    if topic is None:
        topic = ['credit_card']
    model = model_persistence.load_model_from_file(model_path)
    # topic = ['credit_card']
    transaction = kafka_consumer.create_DStream_from_kafka(
        _spark_context, topic)
    ssc = StreamingContext(_spark_context, batchDuration=1)
    transaction.foreachRDD(detect_one(transaction, _spark_session, model))

    # Start the computation
    ssc.start()

    # Wait for the computation to terminate
    ssc.awaitTermination()
