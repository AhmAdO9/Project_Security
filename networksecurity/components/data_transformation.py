from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import os
import sys
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline  import            DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
        DataValidationArtifact, 
        DataTransformationArtifact)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.utils import (
        save_object,
        save_numpy_array_data
)
from networksecurity.constants.training_pipeline import FINAL_MODEL_DIR

class DataTransformation:
    def __init__(self, 
                data_transformation_config:DataTransformationConfig,
                data_validation_artifact:DataValidationArtifact):

        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformer_object(self)->Pipeline:
        try:
            logging.info('Entered get_data_transformer_object method')
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            
            preprocessor:Pipeline = Pipeline(
                steps = [("imputer", imputer)]
            )

            return preprocessor

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Entered_initiate_data_transformation method")
           
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            input_features_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            input_features_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformer_object()

            preprocessor_object = preprocessor.fit(input_features_train_df)
            
            preprocessed_input_features_train_df = preprocessor_object.transform(input_features_train_df)
            preprocessed_input_features_test_df = preprocessor_object.transform(input_features_test_df)

            train_arr = np.c_[preprocessed_input_features_train_df, np.array(target_feature_train_df)]
            test_arr = np.c_[preprocessed_input_features_test_df, np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

            save_object(self.data_transformation_config.transformed_object_file_path, obj=preprocessor_object)
            
            # final preprocessor
            save_object(file_path=f"{FINAL_MODEL_DIR}/preprocessor.pkl", obj=preprocessor_object)


            

            data_transformation_artifact:DataTransformationArtifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path,
            
            )

            return data_transformation_artifact
            

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        