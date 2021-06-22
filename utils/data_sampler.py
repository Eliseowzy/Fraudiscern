# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: data_sampler.py
@time: 6/20/2021
@version: 1.0
"""

import pandas as pd
import time
import spark_manager
import random
import numpy as np
from pyspark.sql import Row
from sklearn import neighbors
from pyspark.ml.feature import VectorAssembler

_spark_session = spark_manager.get_spark_session()


def _extract_numerical_attributes(data_set):
    attributes = data_set.columns
    attributes_type = {}
    for attribute in attributes:
        tmp = str(data_set.schema[attribute]).split(',')
        if tmp[1] == "IntegerType" or tmp[1] == "DoubleType":
            attributes_type[attribute] = tmp[1]
    return attributes_type


def _get_label_proportion(data_set, target):
    target_value = data_set[target].values
    target_count = data_set.groupby(target).count()
    label_proportion = {}
    for value in target_value:
        label_proportion[value] = int(target_count[target_count[target] == 0]["count"])
    return label_proportion


def _vectorize(data_set, target_name):
    column_names = list(_extract_numerical_attributes(data_set).keys())
    dataInput = data_set.select((','.join(column_names) + ',' + target_name).split(','))
    assembler = VectorAssembler(inputCols=column_names, outputCol='features')
    pos_vectorized = assembler.transform(dataInput)
    vectorized = pos_vectorized.select('features', target_name).withColumn('label', pos_vectorized[target_name]).drop(
        target_name)
    return vectorized


def _smote_sampling(vectorized, k=5, minority_class=1, majority_class=0, percentage_over=100, percentage_under=20):
    if percentage_under > 100 or percentage_under < 10:
        raise ValueError('Percentage Under must be in range 10 - 100')
    if percentage_over < 100:
        raise ValueError("Percentage Over must be in at least 100")
    dataInput_min = vectorized[vectorized['label'] == minority_class]
    dataInput_maj = vectorized[vectorized['label'] == majority_class]
    feature = dataInput_min.select('features')
    feature = feature.rdd
    feature = feature.map(lambda x: x[0])
    feature = feature.collect()
    feature = np.asarray(feature)
    nbrs = neighbors.NearestNeighbors(n_neighbors=k, algorithm='auto').fit(feature)
    neighbours = nbrs.kneighbors(feature)
    gap = neighbours[0]
    neighbours = neighbours[1]
    min_rdd = dataInput_min.drop('label').rdd
    pos_rddArray = min_rdd.map(lambda x: list(x))
    pos_ListArray = pos_rddArray.collect()
    min_Array = list(pos_ListArray)
    new_rows = []
    nt = len(min_Array)
    nexs = int(percentage_over / 100)
    for i in range(nt):
        for j in range(nexs):
            neigh = random.randint(1, k)
            difs = min_Array[neigh][0] - min_Array[i][0]
            new_rec = (min_Array[i][0] + random.random() * difs)
            new_rows.insert(0, new_rec)
    new_data_rdd = _spark_session.sparkContext.parallelize(new_rows)
    new_data_rdd_new = new_data_rdd.map(lambda x: Row(features=x, label=1))
    new_data = new_data_rdd_new.toDF()
    new_data_minor = dataInput_min.unionAll(new_data)
    new_data_major = dataInput_maj.sample(False, (float(percentage_under) / float(100)))
    return new_data_major.unionAll(new_data_minor)


def sampler(data_set, target='label'):
    data_set = _spark_session.createDataFrame(data_set)
    label_proportion = _get_label_proportion(data_set, target)
    keys = label_proportion.keys()
    count_1 = label_proportion[keys[0]]
    count_2 = label_proportion[keys[1]]
    ratio = count_1 / count_2
    if ratio > 5:
        # 采样
        new_data_set = _smote_sampling(_vectorize(data_set, 'is_fraud'), k=2, minority_class=1, majority_class=0,
                                       percentage_over=400, percentage_under=5)
    else:
        # 采样
        new_data_set = _smote_sampling(_vectorize(data_set, 'is_fraud'), k=2, minority_class=1, majority_class=0,
                                       percentage_over=400, percentage_under=5)
    return new_data_set
