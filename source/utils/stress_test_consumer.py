# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: stress_test_consumer.py
@time: 7/4/2021
@version:
"""

import json

import cmd_helper
import kafka_manager

_producer_count = 5
_kafka_consumer_result = kafka_manager.get_kafka_consumer(topic="detect_result")
_kafka_consumer_message = kafka_manager.get_kafka_consumer()


def stress_test():
    cmd_helper.help_start_generator(container_count=1)
    _record_count = 0
    _fraud_count = 0
    _normal_count = 0
    for message in _kafka_consumer_result:
        result = json.loads(message.value.decode())
        print(result)
        if result:
            _record_count += 1
            detect_result = json.loads(result)
            detect_label = detect_result["prediction"]
            label = int(detect_label["0"])
            if label:
                _fraud_count += 1
            else:
                _normal_count += 1
    return _record_count, _fraud_count, _normal_count


def main():
    print(stress_test())


if __name__ == '__main__':
    main()
