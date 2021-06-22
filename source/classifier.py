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

# 数据集
_data_set = _spark_session.createDataFrame()
_train_set = _spark_session.createDataFrame()
_test_set = _spark_session.createDataFrame()

# 模型
_model_name = "None"
_model = None


def set_data_set(data_set_path, test_proportion=0.05):
    global _data_set, _train_set, _test_set
    # 导入数据
    _data_set = data_loader.load_data_from_csv(data_set_path)
    # 过采样
    _data_set = data_sampler.smote(_data_set, target='is_fraud')
    # 划分训练集、测试集
    _train_set, _test_set = _get_train_test_set(test_proportion)


def _get_train_test_set(test_proportion=0.05):
    global _data_set
    train_proportion = 1 - test_proportion
    train_set = _data_set.sample(frac=train_proportion, random_state=786)
    test_set = _data_set.drop(train_set.index)
    train_set.reset_index(inplace=True, drop=True)
    test_set.reset_index(inplace=True, drop=True)
    print('Data for Training: ' + str(train_set.shape))
    print('Data for Testing ' + str(test_set.shape))
    return train_set, test_set


def set_model(model_name="random_forest"):
    global _model_name, _model
    if _model_name == "random_forest":
        _model_name = model_name
        # 构造随机森林模型
        _model = random_forest_classifier.RandomForestClassifierModel()

    return _model


def train_model():
    global _model, _model_name, _train_set
    if _model_name == "random_forest":
        _model.fit(_train_set)


def test_model():
    global _model, _model_name, _test_set
    if _model_name == "random_forest":
        _model.predict(_test_set)

# def validate_model():
#     global


# def compare_models(mode_list=None):
#     _logger.info("Compare models is not implemented.")
#     if mode_list is None:
#         mode_list = []
