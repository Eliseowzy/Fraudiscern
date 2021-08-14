# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Zhang Siyu
@file: stress_test_producer.py
@time: 6/21/2021
@version: 1.0
"""

import getpass
import os
import time

import kafka_manager
import time_stamp
from data_generator import generate_transaction_data


def stress_test_kafka_producer(start_date="7-1-2012", end_date="7-31-2012", frequency=0.1):
    """Send simulated transaction data between start_date and end_date to kafka cluster as a producer client.

    Args:
        start_date (str, optional): The start date of the generator. Defaults to "1-1-2012".
        end_date (str, optional): The end date of the generator. Defaults to "7-31-2012".
        frequency (float, optional): The time slot of each message send to kafka. Defaults to 0.1(s).

    Returns:
        [type]: [description]
    """
    producer = kafka_manager.get_kafka_producer()
    transaction_data_set = generate_transaction_data(start_date=start_date, end_date=end_date)
    for _, row in transaction_data_set.iterrows():
        # Send a piece of transaction every 0.1 second.

        row["send_time"] = time_stamp.get_timestamp()
        data = row.to_json()
        time.sleep(frequency)
        producer.send(topic='test_data', value=data)
        print("{} has been send".format(data))
        if _ == 2:
            break
    return None


def main():
    def get_system_username():
        user_name = getpass.getuser()
        return str(user_name)

    output = "Transaction generator on {} has been started!".format(get_system_username())
    os.system('echo -e "\033[31m\033[1m{}\033[0m"'.format(output))
    stress_test_kafka_producer()


if __name__ == '__main__':
    main()
