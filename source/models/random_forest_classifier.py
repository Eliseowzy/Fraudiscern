# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Zhang Siyu, Wang Zhiyi
@file: random_forest_classifier.py
@time: 6/28/2021
@version: 1.1
"""

import matplotlib.pyplot as plt
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator

from curve_metrics import CurveMetrics
# from source.interface import model_interface
from source.interface.model_interface import model_interface
from source.utils import hdfs_manager
from source.utils import logger
from source.utils import model_persistence
from source.utils import spark_manager

_spark_session = spark_manager.get_spark_session()
_hdfs_client = hdfs_manager.get_hdfs_client()
_logger = logger.get_logger()


class RandomForestClassifierModel(model_interface):
    """Implement model interface as random forest classifier model. The functions below, implement the interface definition.

    Args:
        model_interface (ABCMeta): The definition of interface, meta class.
    """

    def __init__(self, impurity='gini', trees_count=200, seed=2021):

        self._model_object = RandomForestClassifier(
            impurity=impurity, numTrees=trees_count, seed=seed)
        self._feature_importance = None

    def __str__(self):
        return str(self._model_object)

    def fit(self, train_set):
        """Train the model

        Args:
            train_set (pyspark.sql.DataFrame): The train set.

        Returns:
            pyspark.ml.classification.RandomForestClassifier: The random forest classifier object.
        """

        self._model_object = self._model_object.fit(train_set)
        self._feature_importance = self._model_object.featureImportances
        print("Feature importance: {}".format(self._feature_importance))
        print(train_set.schema['features'].metadata['ml_attr']['attrs'])
        return self._model_object

    def predict(self, test_set):
        """Use the existing model to predict on a feature data set.

        Args:
            test_set (pyspark.sql.DataFrame): The features will be predicted.

        Returns:
            pyspark.sql.DataFrame: The predict result.
        """
        # print("start predict")
        _predict_result = self._model_object.transform(test_set)

        return _predict_result

    def validate_model(self, test_set, method='accuracy'):
        """Validate the model in some indexes: ['accuracy', 'auc']

        Args:
            test_set:
            method (str, optional): The validation option. Defaults to 'accuracy'.

        Returns:
            multi type: The predict result, could be a value, dictionary etc.
        """
        _predict_result = self._model_object.transform(test_set)
        print("Start validation.")
        _valid_result = 0
        # acc = MulticlassClassificationEvaluator(labelCol='label', metricName='accuracy').evaluate(_predict_result)
        # print("accuracy is {}".format(acc))
        if method == 'accuracy':
            # evaluator = MulticlassClassificationEvaluator.setMetricName(
            #     "accuracy")
            # acc = evaluator.evaluate(_predict_result)
            acc = MulticlassClassificationEvaluator(labelCol='label', metricName='accuracy').evaluate(_predict_result)
            print("accuracy is {}".format(acc))
            _valid_result = acc
        if method == 'auc':
            auc = BinaryClassificationEvaluator(labelCol='label').evaluate(_predict_result)
            # evaluator = BinaryClassificationEvaluator().setMetricName("areaUnderROC").setRawPredictionCol(
            #     'rawPrediction').setLabelCol("label")
            # auc = evaluator.evaluate(_predict_result)
            print("auc is {}".format(auc))

            # Returns as a list (false positive rate, true positive rate)
            _predictions = _predict_result.select('label', 'probability').rdd.map(
                lambda row: (float(row['probability'][1]), float(row['label'])))
            points = CurveMetrics(_predictions).get_curve('roc')

            plt.figure()
            x_val = [x[0] for x in points]
            y_val = [x[1] for x in points]
            plt.title("ROC")
            plt.xlabel("FP")
            plt.ylabel("TP")
            plt.plot(x_val, y_val)
            plt.savefig("roc_curve.png")
            _valid_result = auc
        if method == 'precision':
            precision = MulticlassClassificationEvaluator(labelCol='label',
                                                          metricName='weightedPrecision').evaluate(_predict_result)
            _valid_result = precision
            print("precision is {}".format(precision))
        if method == 'recall':
            recall = MulticlassClassificationEvaluator(labelCol='label', metricName='weightedRecall').evaluate(
                _predict_result)
            _valid_result = recall
            print("recall is {}".format(recall))
        return _valid_result

    def save_model(self, path):
        """Save the trained model into a pickle file.

        Args:
            path (str): The target path to save the model, an hdfs path could be convenient.

        Returns:
            NoneType: None.
        """
        print("测试mode_persistence!!!!!!!")
        print("模型: {}已经保存。".format(self._model_object))
        model_persistence.load_model_to_file(self._model_object, path)
        return None

    def load_model(self, path):
        """Save the trained model from a pickle file.

        Args:
            path (str): The source path to load the model, an hdfs path could be convenient.

        Returns:
            NoneType: None.
        """
        self._model_object = model_persistence.load_model_from_file(path)
        return None

    def get_model_from_memory(self):
        if self._model_object:
            return self._model_object
