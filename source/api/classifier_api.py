# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: 
@file: classifier_api.py
@time: 6/30/2021
@version:
"""
from source.classifier import classifier


def create_classifier():
    classifier_instance = classifier()
    return classifier_instance


def main():
    data_set_path = 'hdfs:///dataset/dataset_1/'
    classifier_instance = create_classifier()
    classifier_instance.set_data_set(data_set_path=data_set_path)
    model = classifier_instance.train_model()
    predict_result = classifier_instance.predict()
    classifier_instance.predict()


if __name__ == '__main__':
    main()
