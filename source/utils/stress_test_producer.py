# -*- coding: utf-8 -*-
"""
# Name: stress_test_producer.py
# Developer: Zhang Siyu
# Data: 23.06.2021
# Version: v1
"""

import getpass
import os
import time

import kafka_manager
import time_stamp
from data_generator import generate_transaction_data


def stress_test_kafka_producer(start_date="1-1-2012", end_date="7-31-2012", frequency=0.1):
    """Send transaction data to kafka cluster as a producer client

    """
    producer = kafka_manager.get_kafka_producer()
    transaction_data_set = generate_transaction_data(start_date=start_date, end_date=end_date)
    for index, row in transaction_data_set.iterrows():
        # Send a piece of transaction every 0.1 second.

        row["send_time"] = time_stamp.get_timestamp()
        data = row.to_json()
        time.sleep(frequency)
        producer.send(topic='test_data', value=data)
        print("{} has been send".format(data))
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
