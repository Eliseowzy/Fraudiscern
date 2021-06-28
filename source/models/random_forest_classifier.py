# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Zhang Siyu, Wang Zhiyi
@file: random_forest_classifier.py
@time: 6/28/2021
@version: 1.1
"""

from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
from pyspark.ml.feature import VectorAssembler

from source.interface.model_interface import model_interface
from source.utils import hdfs_manager
from source.utils import logger
from source.utils import model_persistence
from source.utils import spark_manager

_spark_session = spark_manager.get_spark_session()
_hdfs_client = hdfs_manager.get_hdfs_client()
_logger = logger.get_logger()


class RandomForestClassifierModel(model_interface):
    """
    This is an example for implementing the models interface
    """

    def __init__(self, impurity='gini', trees_count=200, seed=2021):

        self._model_object = RandomForestClassifier(impurity=impurity, numTrees=trees_count, seed=seed)
        self._predict_result = None
        self._feature_importance = None

    def __str__(self):
        return str(self._model_object)

    def fit(self, train_set):
        features = train_set.columns[:-1]
        feature_assembler = VectorAssembler().setInputCols(features).setOutputCol('features')
        pipeline = Pipeline(stages=[feature_assembler, self._model_object])
        self._model_object = pipeline.fit(train_set)
        self._feature_importance = self._model_object.featureImportances
        return self._model_object

    def predict(self, test_set):
        self._predict_result = self._model_object.transform(test_set)
        return self._predict_result

    def validate_model(self, method='accuracy'):
        if method == 'accuracy':
            evaluator = MulticlassClassificationEvaluator.setMetricName("accuracy")
            acc = evaluator.evaluate(self._model_object)
            return acc
        if method == 'auc':
            evaluator = BinaryClassificationEvaluator().setMetricName("areaUnderROC").setRawPredictionCol(
                'rawPrediction').setLabelCol("label")
            auc = evaluator.evaluate(self._predict_result)
            return auc

    def save_model(self, path):
        model_persistence.load_model_to_file(self._model_object, path)
        return None

    def load_model(self, path):
        self._model_object = model_persistence.load_model_from_file(path)
        return None

    def optional_property(self):
        print("You can write some other unique functions here")
