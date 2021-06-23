# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: classifier.py
@time: 6/20/2021
@version: 1.0
"""

from source.models import random_forest_classifier
from source.utils import logger, spark_manager, data_sampler, data_loader, hdfs_manager

# 日志, spark, hdfs单例
_logger = logger.get_logger()
_spark_session = spark_manager.get_spark_session()
_hdfs_client = hdfs_manager.get_hdfs_client()


class classifier:
    def __init__(self, data_set_path):
        # 数据集
        self._data_set = _spark_session.createDataFrame()
        self._train_set = _spark_session.createDataFrame()
        self._test_set = _spark_session.createDataFrame()

        # 模型
        self._model_name = "None"
        self._model = None

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
        # 过采样
        self._data_set = data_sampler.smote(self._data_set, target='is_fraud')
        # 划分训练集、测试集
        self._train_set, self._test_set = self._get_train_test_set(test_proportion)
        return None

    def _get_train_test_set(self, test_proportion=0.05):
        train_proportion = 1 - test_proportion
        train_set = self._data_set.sample(frac=train_proportion, random_state=786)
        test_set = self._data_set.drop(train_set.index)
        train_set.reset_index(inplace=True, drop=True)
        test_set.reset_index(inplace=True, drop=True)
        print('Data for Training: ' + str(train_set.shape))
        print('Data for Testing ' + str(test_set.shape))
        return train_set, test_set

    def set_model(self, model_name="random_forest"):
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
            self._model = random_forest_classifier.RandomForestClassifierModel()
        return self._model

    def train_model(self):
        """
        Train the classifier using train set.

        Returns:
            NoneType: None
        """
        if self._model_name == "random_forest":
            self._model.fit(self._train_set)

        return None

    def test_model(self):
        """
        Test the classifier using test set.

        Returns:
            NoneType: None
        """
        if self._model_name == "random_forest":
            self._model.predict(self._test_set)
        return None

# def validate_model():
#     global


# def compare_models(mode_list=None):
#     _logger.info("Compare models is not implemented.")
#     if mode_list is None:
#         mode_list = []
