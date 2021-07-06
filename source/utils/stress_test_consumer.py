# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: stress_test_consumer.py
@time: 7/4/2021
@version:
"""
import json

import kafka_manager


def stress_test_consumer():
    """ Print messages from kafka cluster as a consumer client
    """
    consumer = kafka_manager.get_kafka_consumer()
    for message in consumer:
        message_content = json.loads(message.value.decode())
        message_topic = message.topic
        print("received:")
        print(message_topic)
        print(message_content)


def main():
    stress_test_consumer()


if __name__ == '__main__':
    main()
