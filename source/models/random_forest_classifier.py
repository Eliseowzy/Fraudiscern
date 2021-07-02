# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Zhang Siyu, Wang Zhiyi
@file: random_forest_classifier.py
@time: 6/28/2021
@version: 1.1
"""

from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator

from source.interface import model_interface
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
        self._predict_result = None
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
        return self._model_object

    def predict(self, test_set):
        """Use the existing model to predict on a feature data set.

        Args:
            test_set (pyspark.sql.DataFrame): The features will be predicted.

        Returns:
            pyspark.sql.DataFrame: The predict result.
        """
        self._predict_result = self._model_object.transform(test_set)
        return self._predict_result

    def validate_model(self, method='accuracy'):
        """Validate the model in some indexes: ['accuracy', 'auc']

        Args:
            method (str, optional): The validation option. Defaults to 'accuracy'.

        Returns:
            multi type: The predict result, could be a value, dictionary etc.
        """
        if method == 'accuracy':
            evaluator = MulticlassClassificationEvaluator.setMetricName(
                "accuracy")
            acc = evaluator.evaluate(self._model_object)
            return acc
        if method == 'auc':
            evaluator = BinaryClassificationEvaluator().setMetricName("areaUnderROC").setRawPredictionCol(
                'rawPrediction').setLabelCol("label")
            auc = evaluator.evaluate(self._predict_result)
            return auc

    def save_model(self, path):
        """Save the trained model into a pickle file.

        Args:
            path (str): The target path to save the model, an hdfs path could be convenient.

        Returns:
            NoneType: None.
        """
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

    def optional_property(self):
        """An optional property implementation, no features has been added.
        """
        print("You can write some other unique functions here")
