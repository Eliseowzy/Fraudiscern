# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: classifier.py
@time: 6/29/2021
@version: 1.1
"""

from source.models import random_forest_classifier
from source.utils import logger, spark_manager, data_sampler, data_loader, hdfs_manager

# 日志, spark, hdfs单例
_logger = logger.get_logger()
_spark_session = spark_manager.get_spark_session()
_hdfs_client = hdfs_manager.get_hdfs_client()


class classifier:
    def __init__(self, model_name='random_forest', target="is_fraud"):
        # 数据集
        self._data_set = None
        self._train_set, self._test_set = None, None
        self._target = target

        # 模型
        self._model_name = model_name
        if model_name == 'random_forest':
            self._model = random_forest_classifier.RandomForestClassifierModel(impurity='gini', trees_count=200,
                                                                               seed=2021)
        self._predict_result = None

    def set_data_set(self, data_set_path, test_proportion=0.05):
        """
        Set the data set of the classifier.

        Args:
            data_set_path: the location of the data set
            test_proportion: The proportion of test set

        Returns:
            None

        """
        self._data_set = data_loader.load_data_from_csv(data_set_path)
        # 划分训练集、测试集
        self._train_set, self._test_set = self._set_train_test_set(test_proportion)
        # 过采样
        self._train_set = data_sampler.smote(self._train_set, target=self._target)
        return self._train_set, self._test_set

    def _set_train_test_set(self, test_proportion=0.05):
        train_proportion = 1 - test_proportion
        self._train_set, self._test_set = self._data_set.randomSplit([train_proportion, test_proportion])
        return self._train_set, self._test_set

    def _set_model(self, model_name="random_forest"):
        """
        Set the model will be trained.

        Args:
            model_name(string): The name of the model.

        Returns:
            classifier model.
        """
        if self._model_name == "random_forest":
            self._model_name = model_name
            # 构造随机森林模型

        return self._model

    def train_model(self):
        """
        Train the classifier using train set.

        Returns:
            NoneType: None
        """
        if self._model_name == "random_forest":
            self._model.fit(self._train_set)
        return self._model

    def predict(self):
        """
        Test the classifier using test set.

        Returns:
            NoneType: None
        """
        self._predict_result = self._model.predict(self._test_set)
        return self._predict_result

    def validate_model(self, validate_method='accuracy'):
        return self._model.validate_model(method=validate_method)