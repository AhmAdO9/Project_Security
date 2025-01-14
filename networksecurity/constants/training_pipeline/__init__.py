import os
import sys
import numpy as np
import pandas as pd

""" Defining common constant values for training pipeline"""

TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "Artifacts" 
FILE_NAME:str = "phishingData.csv"
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")


""" Data Ingestion related constant values """

DATA_INGESTION_COLLECTION_NAME:str = "NetworkData"
DATA_INGESTION_DATABASE_NAME:str = "FaheemAI"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store" # this will store the raw data 
DATA_INGESTION_INGESTED_DIR:str = "ingested" # this will store the train and test data
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2



""" Data Validation related constant values """

DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"


""" Data Transformation related constant values """

DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"
PREPROCESSED_OBJECT_FILE_PATH:str =  "preprocessor.pkl"

# KNN imputer class to replace nan values - it will replace the missing values by calculating the average of 3 nearest neighbors.
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict = {
            "missing_values":np.nan,
            "n_neighbors":3,
            "weights":"uniform",

}

""" Model Trainer related constant values """

MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6

# if the difference between the scores of a model in training and test is more than 0.05, we reject it.
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float = 0.05

SAVED_MODEL_DIR = os.path.join("saved_models")


FINAL_MODEL_DIR:str = "final_model"



