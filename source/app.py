# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: app.py
@time: 7/6/2021
@version:
"""
import json
from time import sleep

import pandas
import pyspark.sql
from flask import Flask, jsonify
from flask_cors import *
from werkzeug.utils import secure_filename

import data_loader
import data_sampler
import hdfs_manager
from classifier import classifier

app = Flask(__name__)
CORS(app, supports_credentials=True)
# 上传文件夹设定
app.config['UPLOAD_FOLDER'] = "/home/hduser/fraudiscern/upload_buffer/"
_data_set: pyspark.sql.DataFrame = None
_data_set_description: pandas.DataFrame = pandas.DataFrame()
_classifier_instance: classifier = classifier()
_hdfs_client = hdfs_manager.get_hdfs_client()

_hdfs_config = {"hdfs_base": "hdfs://10.244.35.208:9000/",
                "hdfs_root": "/dataset/",
                "hdfs_folder_name": "",
                "hdfs_data_set_name": "fraudTest.csv",
                "hdfs_model_name": ""}
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
        source_path = _hdfs_config["hdfs_base"] + _hdfs_config["hdfs_root"] + _hdfs_config["hdfs_folder_name"] + '/' + \
                      _hdfs_config[
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


# @app.route('/', methods=["GET", "POST"])
# def welcome():
#     global _hdfs_config
#     user_name = request.json["user_name")
#     user_id = request.json["user_id")
#     if user_name and user_id:
#         _hdfs_config["hdfs_folder_name"] = "user_{}".format(str(user_id))
#         res = hdfs_manager.create_dir(hdfs_root=_hdfs_config["hdfs_root"], folder_name=_hdfs_config["hdfs_folder_name"])
#         return '''
#         <!DOCTYPE html>
#         <h1>Welcome to fraudiscern! Your user name is {}, your user_id is {}, you have created an hdfs folder: {}</h1>
#         <h2>Congratulations, {}</h2>
#         '''.format(user_name, user_id, _hdfs_config["hdfs_folder_name"], res)
#     else:
#         return '''
#         <!DOCTYPE html>
#         <h1>Welcome to fraudiscern!</h1>
#         <h2>Enjoy it~</h2>
#         '''


# @app.route('/test', methods=["GET", "POST"])
# def index():
# print(len(request.data))

# print(type(request.data))
# print(type(request.json))
# print(request.data)
# print(request)
# print()
# request_json = str(request.json, encoding="utf-8")
# request_json = request.json
# user_name = request_json["user_name"]
# password = request_json["password"]
# print(request_json)
# print(type(request_json))
# res = "user_name: {}, password: {}".format(user_name, password)
# print(res)
# return res
# return render_template('index.html')


html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>Choose Your Dataset:</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

from flask import request
from flask_mail import Mail, Message
import os
from threading import Thread
from utils import user_register

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '863840917@qq.com'
app.config['MAIL_PASSWORD'] = 'uxjvbcwftyambdai'

mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


_auth_code = None


@app.route('/send_auth_code', methods=["GET", "POST"])
def send_auth_code():
    global _auth_code
    print(request.json)
    mail_address = request.json["mail"]
    msg = Message('Welcome {} to fraudiscern!'.format(mail_address), sender='863840917@qq.com',
                  recipients=[mail_address])
    _auth_code = user_register.get_authentication_code(6)
    msg.body = _auth_code
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return str("{status: 'ok'}")


@app.route('/register', methods=["GET", "POST"])
def register():
    from utils import user_register
    global _auth_code

    user_dct = {
        "user_name": request.json["user_name"],
        "mail_address": request.json["mail"],
        "auth_code": request.json["captcha"],
        "password1": request.json["password1"],
        "password2": request.json["password2"]
    }
    # if user_dct["auth_code"] == _auth_code:
    if True:
        if user_dct["password1"] == user_dct["password2"]:
            result = user_register.add_user(user_dct)
            if result:
                #     global _hdfs_config
                #     user_name = request.json["user_name"]
                #     user_id = request.json["user_id"]
                #     if user_name and user_id:
                #         _hdfs_config["hdfs_folder_name"] = "user_{}".format(str(user_id))
                #         res = hdfs_manager.create_dir(hdfs_root=_hdfs_config["hdfs_root"],
                #                                       folder_name=_hdfs_config["hdfs_folder_name"])
                return str("{status: 'ok'}")
            else:
                return str("{status: 'user already exists'}")
    else:
        return str("{status: 'auth code does not match'}")


@app.route('/login', methods=["GET", "POST"])
def login():
    user_name = request.json["user_name"]
    password = request.json["password"]

    return "Login"


@app.route('/upload', methods=["GET", "POST"])
def upload():
    global _hdfs_config, _hdfs_client, _data_set_description
    global _data_set_description

    if request.method == "POST":
        file_object = request.files['file']
        if file_object:
            print(request.files)

            file_name = secure_filename(file_object.filename)
            word_list = file_name.split('.')
            if word_list[1] != 'csv':
                return "Only support .csv format data set!"

            _hdfs_config["hdfs_data_set_name"] = file_name

            # Upload file to server buffer.
            if not os.path.exists(app.config['UPLOAD_FOLDER'] + file_name):
                file_object.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            sleep(1)
            # Compose hdfs_address.
            hdfs_path_to_folder = _hdfs_config["hdfs_root"] + _hdfs_config[
                "hdfs_folder_name"]
            # 从服务器缓冲区上传到hdfs, 子线程上传, 目前在flask中执行shell脚本的功能还无法较好的实现
            # Upload to hdfs
            # import cmd_helper
            # cmd_helper.cmd_helper("hadoop fs -put {} {}".format(app.config['UPLOAD_FOLDER'] + file_name,
            #                                                     hdfs_path_to_folder + '/' + file_name))
            target_path = hdfs_path_to_folder + '/' + file_name
            source_path = app.config['UPLOAD_FOLDER'] + file_name
            hdfs_manager.synchronize_file(hdfs_path=target_path, local_path=source_path)
            # _hdfs_client.upload("/dataset/user_12345/analyzer.py", app.config['UPLOAD_FOLDER'] + file_name)
            _is_finished["load_data_set"] = True
            # return html + "Upload finished!" + "hadoop fs -put {}  {}".format(app.config['UPLOAD_FOLDER'] + file_name,
            #                                                                   hdfs_path_to_folder + '/' + file_name)
            _init_load_data()
            return _data_set_description
        else:
            return "Cannot upload empty file."
    # Make buffer dictionary.
    # 尚未解决如何让flask执行shell脚本，
    # import cmd_helper
    # cmd_helper.cmd_helper("mkdir {}".format(app.config['UPLOAD_FOLDER']))
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    return html + "File will be uploaded to:" + app.config['UPLOAD_FOLDER']


@app.route('/visualization', methods=["GET", "POST"])
def visualization():
    global _data_set
    if not request.json["select_file"]:
        # 获取hdfs文件下的所有文件名
        hdfs_path = _hdfs_config["hdfs_base"] + _hdfs_config["hdfs_folder_name"]
        file_names = hdfs_manager.get_file_names(hdfs_path)
        return file_names
    if request.json["select_file"]:
        # 返回前几行
        file_name = request.json["select_file"]
        _hdfs_config["hdfs_data_set_name"] = file_name
        hdfs_path = _hdfs_config["hdfs_root"] + _hdfs_config["hdfs_folder_name"] + _hdfs_config["hdfs_data_set_name"]
        _data_set = data_loader.load_data_from_hdfs(path=hdfs_path)
        _data_set_tmp = _data_set.toPandas()
        _data_set_tmp = pandas.DataFrame(_data_set_tmp)
        _count = len(_data_set_tmp)
        _result = ""
        if _count > 1000:

            _result = _data_set_tmp.head(1000)
        else:
            _result = _data_set_tmp
        _result = _data_set_tmp.to_json()
        _result = json.dumps(_result)
        return _result


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


@app.route('/train_model', methods=['GET', 'POST'])
def train_model():
    global _classifier_instance, _hdfs_config
    if request.json["model_name"]:
        model_name = request.json["model_name"]
        target = request.json["target"]
        test_ratio = float(request.json["test_ratio"])
        if model_name == "random_forest" and target and test_ratio:
            _classifier_instance = classifier(model_name=model_name, target=target)
            data_set_path = _hdfs_config["hdfs_base"] + _hdfs_config["hdfs_root"] + _hdfs_config["hdfs_folder_name"] + \
                            _hdfs_config["hdfs_data_set_name"]
            _classifier_instance.set_data_set(data_set_path=data_set_path, test_proportion=test_ratio)
            _classifier_instance.train_model()

            hdfs_path_to_folder = _hdfs_config["hdfs_root"] + _hdfs_config[
                "hdfs_folder_name"]
            # 从服务器缓冲区上传到hdfs, 子线程上传, 目前在flask中执行shell脚本的功能还无法较好的实现
            # Upload to hdfs
            # import cmd_helper
            # cmd_helper.cmd_helper("hadoop fs -put {} {}".format(app.config['UPLOAD_FOLDER'] + file_name,
            #                                                     hdfs_path_to_folder + '/' + file_name))
            target_path = hdfs_path_to_folder + '/' + "roc_curve.png"
            source_path = "roc_curve.png"
            hdfs_manager.synchronize_file(hdfs_path=target_path, local_path=source_path)
            _classifier_instance.validate_model(validate_method='precision')
            _classifier_instance.validate_model(validate_method='recall')
            _predict_result = {
                "accuracy": _classifier_instance.validate_model(validate_method='accuracy'),
                "auc": _classifier_instance.validate_model(validate_method='auc'),
                "precision": _classifier_instance.validate_model(validate_method='precision'),
                "recall": _classifier_instance.validate_model(validate_method='recall'),
                "roc": "roc_curve.png"
            }
            return json.dumps(_predict_result)


@app.route('/generator', methods=['GET', 'POST'])
def generator():
    global _classifier_instance, _hdfs_config
    # receive start_date and end_date
    start_date = request.json["start_date"]
    end_date = request.json["end_date"]
    # count = request.json["count")
    frequency = request.json["frequency"]
    if start_date and end_date and frequency:
        import stress_test_producer, fraud_detector
        # 是不是并行的？
        # 多次刷新如何处理？
        fraud_detector.detect()
        stress_test_producer.stress_test_kafka_producer(start_date=start_date, end_date=end_date, frequency=frequency)
    return str("ok")


import kafka_manager

_kafka_consumer_result = kafka_manager.get_kafka_consumer(topic="detect_result")
_kafka_consumer_message = kafka_manager.get_kafka_consumer()


# 先调用generator
# 再调用refresh
@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    # 轮播模块
    import json
    _buffer_window = []

    _record_count = 0
    _fraud_count = 0
    _normal_count = 0
    detect_result = {"record_count": None,
                     "fraud_count": None,
                     "normal_count": None,
                     "messages": None,
                     "prediction": None}
    for message in _kafka_consumer_result:
        result = json.loads(message.value.decode())
        result.replace("\'", "\"")
        # print(type(result))
        # print(result)
        result = json.loads(result)
        if result:
            _record_count += 1
            label = result["prediction"]
            if label:
                _fraud_count += 1
            else:
                _normal_count += 1
            _buffer_window.append(result["current_message"])

            detect_result["record_count"] = _record_count
            detect_result["fraud_count"] = _fraud_count
            detect_result["normal_count"] = _normal_count
            detect_result["messages"] = _buffer_window
            detect_result["prediction"] = label
            return detect_result


if __name__ == '__main__':
    app.run('0.0.0.0', port=20000, debug=True)
