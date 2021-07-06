# -*- coding: utf-8 -*-
"""
# Name: stress_test_producer.py
# Developer: Zhang Siyu
# Data: 23.06.2021
# Version: v1
"""

import time

import kafka_manager
# from pyspark import SparkContext
# from pyspark.streaming import StreamingContext
# from pyspark.streaming.kafka import KafkaUtils
from data_generator import generate_transaction_data


def stress_test_kafka_producer():
    """Send transaction data to kafka cluster as a producer client

    """
    producer = kafka_manager.get_kafka_producer()
    transaction_data_set = generate_transaction_data()
    for index, row in transaction_data_set.iterrows():
        time.sleep(0.5)  # Send a piece of transaction every 0.1 second.
        data = row.to_json()

        producer.send(topic='test_data', value=data)
        print("{} has been send".format(data))
    return None


def main():
    stress_test_kafka_producer()


if __name__ == '__main__':
    main()
