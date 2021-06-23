# -*- coding: utf-8 -*-
"""
# Name: kafka_consumer.py
# Developer: Zhang Siyu
# Data: 23.06.2021
# Version: v1
"""


# from pyspark import SparkContext
# from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def create_DStream_from_kafka(sparkContext, topic):
    '''

    Parameters
    ----------
    sparkContext : object
        spark Context.
    topic :String
        the name of the subscribe topic in kafka.

    Returns
    -------
    A DStream object.

    '''
    
     # ssc = StreamingContext(sparkSession, 5)
    brokers= "spark-797d5ccdb-2d4wd:9092,spark-797d5ccdb-2jmdw:9092,spark-797d5ccdb-4sq79:9092,spark-797d5ccdb-6hsdc:9092,spark-797d5ccdb-72z2j:9092,spark-797d5ccdb-9qz5w:9092,spark-797d5ccdb-c56g9:9092,spark-797d5ccdb-csq2m:9092,spark-797d5ccdb-fjmbr:9092,spark-797d5ccdb-h2hcq:9092,spark-797d5ccdb-ht7vz:9092,spark-797d5ccdb-kvsrm:9092,spark-797d5ccdb-l7txm:9092,spark-797d5ccdb-ln2xr:9092,spark-797d5ccdb-m6ctm:9092,spark-797d5ccdb-m92qw:9092,spark-797d5ccdb-n2sr7:9092,spark-797d5ccdb-p86qx:9092,spark-797d5ccdb-ph9lc:9092,spark-797d5ccdb-pzz6s:9092,spark-797d5ccdb-r78mv:9092,spark-797d5ccdb-rjb6h:9092,spark-797d5ccdb-s2hb2:9092,spark-797d5ccdb-s7fw6:9092,spark-797d5ccdb-s8jdd:9092,spark-797d5ccdb-vp48k:9092,spark-797d5ccdb-vt9c7:9092,spark-797d5ccdb-x84dm:9092,spark-797d5ccdb-xbwtr:9092,spark-797d5ccdb-xwtgf:9092,spark-797d5ccdb-zgsg4:9092,spark-797d5ccdb-zsk59:9092"
    
    consumer = KafkaUtils.createDirectStream(sparkContext, [topic], {"metadata.broker.list": brokers})
    
    return consumer