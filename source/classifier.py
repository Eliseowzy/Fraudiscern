# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: classifier.py
@time: 6/29/2021
@version: 1.1
"""

import json

from pyspark.sql.functions import col
from pyspark.sql.types import DoubleType

import kafka_manager
import spark_manager
from source.models.random_forest_classifier import RandomForestClassifierModel
from source.utils import logger, data_sampler, data_loader, hdfs_manager

# 日志, spark, hdfs单例
_logger = logger.get_logger()
_spark_session = spark_manager.get_spark_session()
_hdfs_client = hdfs_manager.get_hdfs_client()
_spark_context = _spark_session.sparkContext


class classifier:
    def __init__(self, model_name='random_forest', target="is_fraud"):
        # 数据集
        self._data_set = None
        self._data_schema = None
        self._train_set, self._test_set = None, None
        self._target = target

        # ml model
        self._model_name = model_name
        # factory pattern
        if model_name == 'random_forest':
            self._model = RandomForestClassifierModel()
        self._predict_result = None

    def __str__(self):
        return "{}: {}".format(str(self._model_name), str(self._model))

    def set_data_set(self, data_set_path, test_proportion=0.05):
        """
        Set the data set of the classifier.

        Args:
            data_set_path: the location of the data set
            test_proportion: The proportion of test set

        Returns:
            None

        """

        self._data_set = data_loader.load_data_from_hdfs(data_set_path)
        # 划分训练集、测试集
        self._train_set, self._test_set = self._set_train_test_set(test_proportion)
        # 过采样
        # self._train_set = data_sampler.smote(
        # self._train_set, target=self._target)
        self._train_set = data_sampler.vectorize(self._train_set, self._target)
        self._test_set = data_sampler.vectorize(self._test_set, self._target)
        return self._train_set, self._test_set

    def _set_train_test_set(self, test_proportion=0.05):
        """Split the train set and test set. The ratio is 0.95~0.05 by default.

        Args:
            test_proportion (float, optional): The ratio fo test set. Defaults to 0.05.

        Returns:
            pyspark.sql.DataFrame, pyspark.sql.DataFrame: Train set, Test set.
        """
        train_proportion = 1 - test_proportion
        self._train_set, self._test_set = self._data_set.randomSplit(
            [train_proportion, test_proportion])
        return self._train_set, self._test_set

    def _set_model(self, model_name="random_forest"):
        """
        Set the model will be trained.

        Args:
            model_name(string): The name of the model.

        Returns:
            pyspark.ml.classification.*: Model object.
        """
        # factory pattern: Compose random forest model
        if self._model_name == "random_forest":
            self._model_name = model_name
            self._model = RandomForestClassifierModel(impurity='gini', trees_count=200,
                                                      seed=2021)
        return self._model

    def train_model(self):
        """
        Train the classifier using train set.

        Returns:
            pyspark.ml.classification.*: Model object
        """
        self._set_model(self._model_name)
        print(self._model_name)
        if self._model_name == "random_forest":
            self._model.fit(self._train_set)
        return self._model

    def predict(self, data_set=None):
        """
        Test the classifier using test set.

        Returns:
            pyspark.sql.DataFrame: predict_result
        """
        if data_set is None:
            self._predict_result = self._model.predict(self._test_set)
            return self._predict_result
        else:
            return self._model.predict(data_set)

    def validate_model(self, validate_method='accuracy'):
        """Validate the model by appointed method.

        Args:
            validate_method (str, optional): The validation method. Defaults to 'accuracy'.

        Returns:
            Multi-type: The predict result, could be a value, dictionary etc.
        """
        return self._model.validate_model(method=validate_method, test_set=self._test_set)

    def save_model(self, path="hdfs://10.244.35.208:9000/models/RandomForestModel/random_forest_1"):
        self._model.save_model(path=path)
        return None

    def load_model(self, path="hdfs://10.244.35.208:9000/models/RandomForestModel/random_forest_1"):
        return self._model.load_model(path=path)

    def load_model_from_memory(self):
        return self._model.get_model_from_memory()

    def detect_fraud(self):
        _kafka_consumer = kafka_manager.get_kafka_consumer()
        for message in _kafka_consumer:
            message_content = json.loads(message.value.decode())
            print("Received message is: {}".format(message_content))
            if message_content:
                message_topic = message.topic
                message_content = _spark_session.read.json(_spark_context.parallelize([message_content]))
                message_content.show()
                for i in message_content.columns:
                    message_content = message_content.withColumn(i, col(i).cast(DoubleType()))
                message_content.show()
                tmp_message = message_content.select(
                    ['amt', 'cc_num', 'city_pop', 'is_fraud', 'lat', 'long', 'merch_lat', 'merch_long', 'unix_time',
                     'zip'])
                tmp_message.show()
                try:
                    tmp_message = _spark_session.createDataFrame(tmp_message)
                except TypeError:
                    pass
                tmp_message = data_sampler.vectorize(tmp_message, target_name='is_fraud')
                detect_result = self.predict(tmp_message)
                print(detect_result)
                detect_result = detect_result.toPandas()
                print(detect_result)
        return
