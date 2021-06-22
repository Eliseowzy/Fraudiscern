#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# Name: data_generator.py
# Developer:
# Date:
# Version:
# ******************************************************************************

import pandas as pd
import time
import spark_manager
import random
import numpy as np
from pyspark.sql import Row
from sklearn import neighbors
from pyspark.ml.feature import VectorAssembler

cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
spark_appName = "{}_{}".format("app", str(cur_time))
_spark = spark_manager.get_spark_session(spark_appName)


def _vectorize(dataset, target_name):
    columnNames = ['amt', 'lat', 'long', 'merch_long', 'is_fraud']
    dataInput = dataset.select((','.join(columnNames) + ',' + target_name).split(','))
    assembler = VectorAssembler(inputCols=columnNames, outputCol='features')
    pos_vectorized = assembler.transform(dataInput)
    vectorized = pos_vectorized.select('features', target_name).withColumn('label', pos_vectorized[target_name]).drop(
        target_name)
    return vectorized


def SmoteSampling(vectorized, k=5, minorityClass=1, majorityClass=0, percentageOver=100, percentageUnder=20):
    if (percentageUnder > 100 | percentageUnder < 10):
        raise ValueError('Percentage Under must be in range 10 - 100');
    if (percentageOver < 100):
        raise ValueError("Percentage Over must be in at least 100");
    dataInput_min = vectorized[vectorized['label'] == minorityClass]
    dataInput_maj = vectorized[vectorized['label'] == majorityClass]
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
    newRows = []
    nt = len(min_Array)
    nexs = int(percentageOver / 100)
    for i in range(nt):
        for j in range(nexs):
            neigh = random.randint(1, k)
            difs = min_Array[neigh][0] - min_Array[i][0]
            newRec = (min_Array[i][0] + random.random() * difs)
            newRows.insert(0, (newRec))
    newData_rdd = _spark.sparkContext.parallelize(newRows)
    newData_rdd_new = newData_rdd.map(lambda x: Row(features=x, label=1))
    new_data = newData_rdd_new.toDF()
    new_data_minor = dataInput_min.unionAll(new_data)
    new_data_major = dataInput_maj.sample(False, (float(percentageUnder) / float(100)))
    return new_data_major.unionAll(new_data_minor)


def sampler(data_set, target='label', categorical_attributes=None):
    data_set = _spark.createDataFrame()
    label_proportion = _get_label_proportion(data_set, target)
    keys = label_proportion.keys()
    count_1 = label_proportion[keys[0]]
    count_2 = label_proportion[keys[1]]
    ratio = count_1 / count_2
    if ratio > 5:
        # 采样的数量
        num = count_1 - count_2
        # 采样
        new_data_set = _smote(data_set, target, type_value=keys[0], sample_num=num,
                              categorical_attributes=categorical_attributes)
    else:
        # 采样的数量
        num = count_2 - count_1
        # 采样
        new_data_set = _smote(data_set, target, type_value=keys[1], sample_num=num,
                              categorical_attributes=categorical_attributes)
    return data_set
