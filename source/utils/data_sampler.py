# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: data_sampler.py
@time: 6/28/2021
@version: 1.1
"""

import random

import numpy as np
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, DoubleType
from sklearn import neighbors

import spark_manager

_spark_session = spark_manager.get_spark_session()


def _get_label_proportion(data_set, target):
    """Get the proportion of each type. Implemented on spark.

    Args:
        data_set (pyspark.sql.dataframe.DataFrame): The data set.
        target (str): The target column.

    Returns:
        label_proportion (dct): A dictionary, (key, values) ~ (attribute, count)
    """
    target_count = data_set.groupby(target).count()
    label_proportion = {}
    target_count = target_count.toPandas()
    for attribute, count in zip(target_count[target], target_count['count']):
        label_proportion[attribute] = count
    return label_proportion


def _extract_numerical_attributes(data_set):
    """Extract numerical attributes. On spark numerical type includes 'IntegerType and DoubleType'.

    Args:
        data_set (pyspark.sql.dataframe.DataFrame): The data set.

    Returns:
        dct: A dictionary, (key, values) ~ (attribute, type)
    """
    attributes = data_set.columns
    attributes = attributes[1:]
    attributes_type = {}
    for attribute in attributes:
        tmp = str(data_set.schema[attribute]).split(',')
        if tmp[1] == "IntegerType" or tmp[1] == "DoubleType":
            attributes_type[attribute] = tmp[1]
    return attributes_type


def _vectorize(data_set, target_name):
    """Extract the numerical attributes then vectorize the data set.

    Args:
        data_set (pyspark.sql.dataframe.DataFrame): The data set.
        target_name (str): The label column of the dataset

    Returns:
        pyspark.sql.dataframe.DataFrame: {features: denseVector(), labels: labels of the attributes.}
    """
    # print(_extract_numerical_attributes(data_set))
    num_cols = _extract_numerical_attributes(data_set).keys()
    num_cols = list(num_cols)
    if data_set.select(target_name).distinct().count() != 2:
        raise ValueError("Target col must have exactly 2 classes")
    if target_name in num_cols:
        num_cols.remove(target_name)
    # only assembled numeric columns into features
    assembler = VectorAssembler(inputCols=num_cols, outputCol='features')
    pipeline = Pipeline(stages=[assembler])
    pos_vectorized = pipeline.fit(data_set).transform(data_set)
    # drop original num cols and cat cols
    # drop_cols = num_cols
    # keep_cols = [a for a in pos_vectorized.columns if a not in drop_cols]
    # vectorized = pos_vectorized.select(*keep_cols).withColumn('label', pos_vectorized[target_name]).drop(target_name)
    vectorized = pos_vectorized.select('features', target_name).withColumn('label', pos_vectorized[target_name]).drop(
        target_name)
    return vectorized


def _split_column(data_set, features: list):
    """Split the data set into a suitable form for training the model.

    Args:
        data_set (pyspark.sql.dataframe.DataFrame): A data frame the structure: {features: denseVector[value_1, value_2, value_3, ...], labels: 1}
        features (str): The column contains attributes.

    Returns:
        pyspark.sql.dataframe.DataFrame: A data frame the structure: {v1: value_1, v2: value_2, v3: value_3,...vn, value_n, labels: 1}
    """
    schema = None
    print("schema是schema是schema是schema是schema是schema是schema是schema是：{}".format(schema))

    def _create_schema_str(_data_set, _features: list):
        str_schema = "schema = StructType(["
        for feature in _features:
            str_schema += "StructField('{}', DoubleType(), True),".format(feature)
        str_schema = str_schema[:-1]
        str_schema += '''])'''

        return str_schema

    schema_str = _create_schema_str(data_set, features)
    print(schema_str+ "是是是是")
    # exec(schema_str)
    # print("schema是schema是schema是schema是schema是schema是schema是schema是：{}".format(schema))
    schema = StructType([StructField('zip', DoubleType(), True), StructField('lat', DoubleType(), True),
                         StructField('long', DoubleType(), True), StructField('city_pop', DoubleType(), True),
                         StructField('unix_time', DoubleType(), True), StructField('merch_lat', DoubleType(), True),
                         StructField('merch_long', DoubleType(), True), StructField('is_fraud', DoubleType(), True)])
    final_df = _spark_session.createDataFrame(
        _spark_session.sparkContext.emptyRDD(), schema)
    for row in data_set.rdd.toLocalIterator():
        tmp_row = list(row["features"])
        tmp_row = [float(i) for i in tmp_row]
        tmp_ls = tuple(tmp_row)
        tmp_df = _spark_session.sparkContext.parallelize(
            [tmp_ls]).toDF(data_set.columns)
        final_df = final_df.union(tmp_df)
    print("Result is:")
    print(final_df.head(1))
    return final_df


def _smote_sampling(vectorized, k=5, minority_class=1, majority_class=0, percentage_over=400, percentage_under=10):
    """Smote sampling on a data set (private function).
    Args:
        vectorized (pyspark.sql.dataframe.DataFrame): The data set.
        k (int, optional): The number of nearest neighbors. Defaults to 5.
        minority_class (int, optional): Majority attribute. Defaults to 1.
        majority_class (int, optional): Minority attribute. Defaults to 0.
        percentage_over (int, optional): Oversampling percentage. Defaults to 100.
        percentage_under (int, optional): Under-sampling percentage. Defaults to 20.
    Raises:
        ValueError: Percentage Under must be in range 10 - 100
        ValueError: Percentage Over must be in at least 100
    Returns:
        pyspark.sql.dataframe.DataFrame: The data set after smote sampling.
    """
    if percentage_under > 100 | percentage_under < 10:
        raise ValueError("Percentage Under must be in range 10 - 100")
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
    #     gap = neighbours[0]
    #     neighbours = neighbours[1]
    min_rdd = dataInput_min.drop('label').rdd
    pos_rddArray = min_rdd.map(lambda x: list(x))
    pos_ListArray = pos_rddArray.collect()
    min_Array = list(pos_ListArray)
    newRows = []
    nt = len(min_Array)
    nexs = int(percentage_over / 100)
    for i in range(nt):
        for j in range(nexs):
            neigh = random.randint(1, k)
            difs = min_Array[neigh][0] - min_Array[i][0]
            newRec = (min_Array[i][0] + random.random() * difs)
            newRows.insert(0, (newRec))
    newData_rdd = _spark_session.sparkContext.parallelize(newRows)
    newData_rdd_new = newData_rdd.map(lambda x: Row(features=x, label=1))
    new_data = newData_rdd_new.toDF()
    new_data_minor = dataInput_min.unionAll(new_data)
    new_data_major = dataInput_maj.sample(False, (float(percentage_under) / float(100)))
    return new_data_major.unionAll(new_data_minor)


def smote(data_set, target='is_fraud'):
    """SMOTE sampling on a dataset.
    Calculate the ratio of fraud and not fraud cases, if the ratio lager than 5, do smote sampling.
    Args:
        data_set: A data set with numerical attributes and one target attribute.
        target: The column index of target attributes.
    Returns:
        new_data_set(pyspark.DataFrame): The data set after sampling.
    """
    label_proportion = _get_label_proportion(data_set, target)
    keys = [i for i in label_proportion.keys()]
    count_1 = label_proportion[keys[0]]
    count_2 = label_proportion[keys[1]]
    ratio = max(count_1, count_2) / min(count_1, count_2)
    new_data_set = None
    if ratio > 5:
        # print("start smote")
        # sampling
        new_data_set = _smote_sampling(_vectorize(data_set, target_name=target))
        # column_names = list(_extract_numerical_attributes(data_set).keys())
        # column_names = column_names[1:]
        # # print(column_names)
        # new_data_set = _split_column(new_data_set, column_names)
    return new_data_set
