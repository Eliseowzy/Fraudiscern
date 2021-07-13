# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: stress_test_consumer.py
@time: 7/13/2021
@version:
"""

import json

import kafka_manager

_producer_count = 5
_kafka_consumer_result = kafka_manager.get_kafka_consumer(topic="detect_result")
_kafka_consumer_message = kafka_manager.get_kafka_consumer()


def stress_test():
    _record_count = 0
    _fraud_count = 0
    _normal_count = 0
    detect_result = {"record_count": None,
                     "fraud_count": None,
                     "normal_count": None,
                     "current_message": None,
                     "prediction": None}
    for message in _kafka_consumer_result:
        result = json.loads(message.value.decode())
        result.replace("\'", "\"")
        # print(type(result))
        # print(result)
        result = json.loads(result)
        if result:
            _record_count += 1
            label = result["prediction"]
            if label:
                _fraud_count += 1
            else:
                _normal_count += 1
            detect_result["record_count"] = _record_count
            detect_result["fraud_count"] = _fraud_count
            detect_result["normal_count"] = _normal_count
            detect_result["current_message"] = result
            detect_result["prediction"] = label
        print(detect_result)
    return


def main():
    print(stress_test())


if __name__ == '__main__':
    main()
