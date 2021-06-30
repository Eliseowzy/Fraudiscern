# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Zhang Siyu, Wang Zhiyi
@file: fraud_detector.py
@time: 6/30/2021
@version: v1.0
"""

import kafka_consumer
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.mllib.util import Loader
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

from source.utils import spark_manager

_spark_session = spark_manager.get_spark_session()
_spark_context = _spark_session.sparkContext


def detect(record, spark, model):
    try:
        record = record.filter(lambda x: len(x) > 0)

        rowRdd = record.map(lambda w: Row(transaction=w))

        recordsDataFrame = spark.createDataFrame(rowRdd)

        model.transform(recordsDataFrame)
    except:
        print('No data')


def main():
    appName = "spark_streaming_test"
    conf = SparkConf() \
        .setAppName(appName) \
        .setMaster('yarn')
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)
    model_path = 'hdfs:///models/RandomForestModel/rf_1'
    model = Loader.load(sc, model_path)
    topic = ['credit_card']
    transaction = kafka_consumer.create_DStream_from_kafka(sc, topic)
    ssc = StreamingContext(sc, batchDuration=1)
    transaction.foreachRDD(detect(transaction, spark, model))

    # Start the computation
    ssc.start()

    # Wait for the computation to terminate
    ssc.awaitTermination()


if __name__ == "__main__":
    main()
