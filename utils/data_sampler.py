#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# Name: data_generator.py
# Developer:
# Date:
# Version:
# ******************************************************************************

import pandas as pd
import spark_manager

_spark = spark_manager.get_spark_session()


def _get_label_proportion(data_set, target='label'):
    data_set = _spark.createDataFrame(data_set)
    label_count = data_set.groupby(target).count()
    row_number = label_count.count()
    print(data_set, row_number)
    # Exception handling: Target attributes are not binary.
    if row_number != 2:
        raise TypeError("Error process: Only support binary targets.")
    iterator = data_set.rdd.toLocalIterator()
    row_1 = next(iterator).count
    row_2 = next(iterator).count
    res = {row_1[target]: row_1['count'], row_2[target]: row_2['count']}
    return res


def _vectorize(data_set, categorical_attributes, target):
    columns = data_set.columns
    columns = list(columns)
    columns.remove(data_set['target'])
    data_set_vectorized = _spark.createDataFrame()
    assembler = VectorAssembler(inputCols=columns, outputCol='features')
    pos_vectorized = assembler.transform(dataInput)
    vectorized = pos_vectorized.select('features', TargetFieldName).withColumn('label',
                                                                               pos_vectorized[TargetFieldName]).drop(
        TargetFieldName)
    return data_set_vectorized


def _smote(data_set, target, type_value, sample_num, categorical_attributes=None):
    # 将数据集向量化
    new_data_set = _vectorize(data_set, categorical_attributes, target)
    # 筛选出需要采样的数据
    new_data_set = data_set.filter(new_data_set[target] == type_value)

    return new_data_set


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
