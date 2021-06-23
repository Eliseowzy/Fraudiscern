# -*- coding: utf-8 -*-
"""
# Name: trian_model.py
# Developer: Zhang Siyu
# Data: 17.06.2021
# Version: v1
"""

# import findspark #行
# findspark.init('/opt/spark-2.4.0-bin-hadoop2.7')
from pyspark.sql import SparkSession
from pyspark import SparkConf

from pyspark.sql.functions import col
from pyspark.sql.types import DoubleType
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
# from pyspark.ml.evaluation import BinaryClassificationEvaluator,MulticlassClassificationEvaluator
from pyspark.ml import Pipeline

def get_spark_session(appName):
    '''
    Parameters
    ----------
    appName : String
        the name of Spark session.

    Returns
    -------
    _SPARK_SESSION : object
        Spark session.

    '''
    global _SPARK_SESSION
    conf = SparkConf()\
        .setMaster("yarn")\
        .setAppName(appName)
    _SPARK_SESSION = SparkSession \
        .builder \
        .config(conf=conf) \
        .getOrCreate()
    return _SPARK_SESSION


def load_data_from_HDFS(spark, path, train_file, test_file):
    '''

    Parameters
    ----------
    spark: object
        Spark Session
    path : String
        Source file directory in HDFS.
    train_file : String
        Name of train dataset.
    test_file : String
        Name of test dataset.

    Returns
    -------
    train_Dataframe, test_Dataframe

    '''
    # load data from HDFS
    #path = 'hdfs:///dataset/dataset_1/'
    #train_file = 'fraudTrain_number.csv'
    #test_file = 'fraudTest_number.csv'
    schema = None
    sep = ','
    header = True
    csvDF_train = spark.read.csv(path = path+train_file, schema = schema ,sep = sep, header = header)
    csvDF_test = spark.read.csv(path = path+test_file, schema = schema ,sep = sep, header = header)
    
    # get features and the label
    for i in csvDF_train.columns:
        csvDF_train = csvDF_train.withColumn(i,col(i).cast(DoubleType()))
        if i == "is_fraud":
            csvDF_train = csvDF_train.withColumnRenamed(i, "label")
    for i in csvDF_test.columns:
        csvDF_test = csvDF_test.withColumn(i,col(i).cast(DoubleType()))
        if i == "is_fraud":
            csvDF_test = csvDF_test.withColumnRenamed(i, "label")
    
    return csvDF_train, csvDF_test

def train_model_RF(csvDF_train, csvDF_test):
    '''

    Parameters
    ----------
    csvDF_train : dataframe
        dataframe for training.
    csvDF_test : dataframe
        dataframe for testing.

    Returns
    -------
    rf_model

    '''
    featuresArray = csvDF_train.columns[:-1]
    assembler = VectorAssembler().setInputCols(featuresArray).setOutputCol("features")
    
    # create a Random Forest Model
    RF = RandomForestClassifier(impurity='gini', numTrees=200,seed=2021).setLabelCol("label").setFeaturesCol("features")
    
    # create a pipeline
    Pipeline_model = Pipeline().setStages([assembler,RF])

    # train the model
    model = Pipeline_model.fit(csvDF_train)
    
    return model

def save_model_to_HDFS(model, path):
    '''

    Parameters
    ----------
    model: object
        ML model
    path : String
        the direcory of saving model in HDFS.

    Returns
    -------
    None.

    '''
    # save the trained RF model to DHFS
    # model.save('hdfs:///models/RandomForestModel/rf_1')
    model.save(path)
    
def main():
    appName = "model_training_test"
    spark = get_spark_session(appName)
    source_path = 'hdfs:///dataset/dataset_1/'
    train_file = 'fraudTrain_number.csv'
    test_file = 'fraudTest_number.csv'
    csvDF_train, csvDF_test = load_data_from_HDFS(spark, source_path, train_file, test_file)
    model = train_model_RF(csvDF_train, csvDF_test)
    target_path = 'hdfs:///models/RandomForestModel/rf_1'
    save_model_to_HDFS(model, target_path)
    
if __name__ == "__main__":
    main()