# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: app.py
@time: 7/6/2021
@version:
"""
import os
import subprocess
from time import sleep

import pandas
import pyspark.sql
from flasgger import Swagger
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

import data_loader
import data_sampler
import hdfs_manager
from classifier import classifier

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "/home/hduser/fraudiscern/upload_buffer/"
_data_set: pyspark.sql.DataFrame = None
_data_set_description: pandas.DataFrame = pandas.DataFrame()
_classifier_instance: classifier = classifier()
_hdfs_client = hdfs_manager.get_hdfs_client()

_hdfs_config = {"hdfs_base": "hdfs://10.244.35.208:9000/",
                "hdfs_root": "/dataset/",
                "hdfs_folder_name": "",
                "hdfs_data_set_name": "fraudTest.csv"}
# bool数据是否导入
_is_finished = {
    "load_data_set": False,
    "describe_data_set": False,
    "preprocess_data_set": False}

# 正例和负例的比例
_data_ratio = {
    "before_smote": pandas.DataFrame(),
    "after_smote": pandas.DataFrame()
}


def _init_load_data():
    global _data_set, _data_set_description, _is_finished, _hdfs_config
    if _is_finished["describe_data_set"]:
        # If the data description has been generated and it is not changed, return it directly.
        return
    else:
        source_path = _hdfs_config["hdfs_base"] + _hdfs_config["hdfs_root"] + _hdfs_config[
            "hdfs_data_set_name"]
        _data_set = data_loader.load_data_from_hdfs(path=source_path)
        _data_set = _data_set.select(["amt", "lat", "long", "city_pop", "merch_lat", "merch_long",
                                      "is_fraud"])
        _data_set_description = _data_set.describe()
        _data_set_description = _data_set_description.toPandas()
        # data_set_description = data_set_description.to_html()
        # data_set_description = str(data_set_description)
        _is_finished["describe_data_set"] = True
        return


def _init_preprocess():
    global _data_set, _data_ratio, _is_finished
    if not _is_finished["load_data_set"] or not _is_finished["describe_data_set"]:
        _init_load_data()
        _init_preprocess()
    else:
        data_set_before = data_sampler.vectorize(data_set=_data_set, target_name='is_fraud')
        _data_ratio["before_smote"] = data_set_before.groupby('label').count().toPandas()
        data_set = data_sampler.smote(_data_set)
        _data_ratio["after_smote"] = data_set.groupby('label').count().toPandas()
        _is_finished["preprocess_data_set"] = True
        return


@app.route('/', methods=["GET", "POST"])
def welcome():
    global _hdfs_config
    user_name = request.form.get("user_name")
    user_id = request.form.get("user_id")
    if user_name and user_id:
        _hdfs_config["hdfs_folder_name"] = "user_{}".format(str(user_id))
        res = hdfs_manager.create_dir(hdfs_root=_hdfs_config["hdfs_root"], folder_name=_hdfs_config["hdfs_folder_name"])
        return '''
        <!DOCTYPE html>
        <h1>Welcome to fraudiscern! Your user name is {}, your user_id is {}, you have created an hdfs folder: {}</h1>
        <h2>Congratulations, {}</h2>
        '''.format(user_name, user_id, _hdfs_config["hdfs_folder_name"], res)
    else:
        return '''
        <!DOCTYPE html>
        <h1>Welcome to fraudiscern!</h1>
        <h2>Enjoy it~</h2>
        '''


html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>Choose Your Dataset:</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


def cmd_helper(cmd):
    # subprocess.check_output([cmd])
    # subprocess.Popen([cmd]).communicate()
    subprocess.call(cmd)


@app.route('/upload', methods=["GET", "POST"])
def upload():
    global _hdfs_config, _hdfs_client
    if request.method == "POST":
        file_object = request.files['file']
        if file_object:
            print(request.files)

            file_name = secure_filename(file_object.filename)

            # 上传到服务器缓冲区
            file_object.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

            sleep(2)
            # 构造hdfs_地址
            hdfs_path_to_folder = _hdfs_config["hdfs_root"] + _hdfs_config[
                "hdfs_folder_name"]
            # 从服务器缓冲区上传到hdfs, 子线程上传
            cmd_helper("hadoop fs -put {} {}".format(app.config['UPLOAD_FOLDER'] + file_name,
                                                     hdfs_path_to_folder + '/' + file_name))
            _is_finished["load_data_set"] = True
            return html + "Upload finished!" + "hadoop fs -put {}  {}".format(app.config['UPLOAD_FOLDER'] + file_name,
                                                                              hdfs_path_to_folder + '/' + file_name)
        else:
            return "Cannot upload empty file."
    # 创建缓冲区目录
    cmd_helper("mkdir {}".format(app.config['UPLOAD_FOLDER']))
    return html + "File will be uploaded to:" + app.config['UPLOAD_FOLDER']


@app.route('/visualization', methods=["GET", "POST"])
def visualization():
    global _data_set_description
    _init_load_data()
    return jsonify(_data_set_description.to_json())


@app.route('/preprocess', methods=["GET", "POST"])
def preprocess():
    global _data_ratio
    _init_preprocess()
    res_ratio = {"before_smote": _data_ratio["before_smote"].to_json(),
                 "after_smote": _data_ratio["after_smote"].to_json()}
    return jsonify(res_ratio)


"""
    classifier_instance = classifier()
    classifier_instance.set_data_set("hdfs://10.244.35.208:9000/dataset/dataset_1/fraudTest.csv")
    # print(test.head(3))
    classifier_instance.train_model()
    classifier_instance.save_model()
    classifier_instance.predict()
    # validation module test
    classifier_instance.validate_model(validate_method='accuracy')
    classifier_instance.validate_model(validate_method='auc')
    classifier_instance.validate_model(validate_method='precision')
    classifier_instance.validate_model(validate_method='recall')
"""


@app.route('/train-model', methods=['GET', 'POST'])
def train_model():
    global _classifier_instance, _hdfs_config
    model_name = request.form.get("model_name")
    target = request.form.get("target")
    _train_ratio = float(request.form.get("train_ratio"))
    classifier_instance = classifier(model_name=model_name, target=target)
    data_set_path = _hdfs_config["hdfs_base"] + _hdfs_config["hdfs_root"] + _hdfs_config["hdfs_folder_name"] + \
                    _hdfs_config["hdfs_data_set_name"]
    classifier_instance.set_data_set(data_set_path=data_set_path)


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
