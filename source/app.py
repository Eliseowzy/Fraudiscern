# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: 
@file: app.py
@time: 7/6/2021
@version:
"""
import pandas
import pyspark.sql
from flasgger import Swagger
from flask import Flask, jsonify

import data_loader
import data_sampler
from classifier import classifier

app = Flask(__name__)

data_set: pyspark.sql.DataFrame = None
data_set_description: pandas.DataFrame = pandas.DataFrame()
# bool数据是否导入
is_finished = {
    "load_data_set": False,
    "describe_data_set": False,
    "preprocess_data_set": False}

# 正例和负例的比例
ratio = {
    "before_smote": pandas.DataFrame(),
    "after_smote": pandas.DataFrame()
}


def init_load_data(source_path="hdfs://10.244.35.208:9000/dataset/dataset_1/fraudTest.csv"):
    global data_set, data_set_description, is_finished
    if is_finished["describe_data_set"] and is_finished["load_data_set"]:
        # If the data description has been generated and it is not changed, return it directly.
        return
    else:
        data_set = data_loader.load_data_from_hdfs(path=source_path)
        data_set = data_set.select(["amt", "lat", "long", "city_pop", "merch_lat", "merch_long",
                                    "is_fraud"])
        data_set_description = data_set.describe()
        data_set_description = data_set_description.toPandas()
        # data_set_description = data_set_description.to_html()
        # data_set_description = str(data_set_description)
        is_finished["load_data_set"] = True
        is_finished["describe_data_set"] = True
        return


def init_preprocess():
    global data_set, ratio, is_finished
    if not is_finished["load_data_set"] or not is_finished["describe_data_set"]:
        init_load_data()
        init_preprocess()
    else:
        data_set_before = data_sampler.vectorize(data_set=data_set, target_name='is_fraud')
        ratio["before_smote"] = data_set_before.groupby('label').count().toPandas()
        data_set = data_sampler.smote(data_set)
        ratio["after_smote"] = data_set.groupby('label').count().toPandas()
        is_finished["preprocess_data_set"] = True
        return


def train_model():
    global is_finished
    if not is_finished["preprocess_data_set"]:
        init_preprocess()
    else:
        test_proportion = 0.85
        data_path = "hdfs://10.244.35.208:9000/dataset/dataset_1/fraudTest.csv"
        classifier_instance = classifier()
        classifier_instance.set_data_set(data_set_path=data_path, test_proportion=test_proportion)
        # print(test.head(3))
        classifier_instance.train_model()
        classifier_instance.save_model()
        classifier_instance.predict()
        # validation module test
        classifier_instance.validate_model(validate_method='accuracy')
        classifier_instance.validate_model(validate_method='auc')
        classifier_instance.validate_model(validate_method='precision')
        classifier_instance.validate_model(validate_method='recall')


@app.route('/')
def welcome():
    return '<h1>Welcome to fraudiscern!</h1>'


@app.route('/visualization')
def visualization():
    global data_set_description
    init_load_data()
    return jsonify(data_set_description.to_json())


@app.route('/preprocess')
def preprocess():
    global ratio
    init_preprocess()
    res_ratio = {"before_smote": ratio["before_smote"].to_json(),
                 "after_smote": ratio["after_smote"].to_json()}
    return jsonify(res_ratio)


swagger = Swagger(app)


@app.route('/colors/<palette>/')
def colors(palette):
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications.
    ---
    parameters:
      - name: palette
        in: path
        type: string
        enum: ['all', 'rgb', 'cmyk']
        required: true
        default: all
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    all_colors = {
        'cmyk': ['cian', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}
    return jsonify(result)


if __name__ == '__main__':
    app.run('0.0.0.0', port=20000, debug=True)
