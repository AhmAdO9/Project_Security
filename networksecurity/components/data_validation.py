from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os, sys
from networksecurity.utils.utils import read_yaml_file
from networksecurity.utils.utils import write_yaml_file



class DataValidation:
    def __init__(
        self, 
        data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact):

        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    @staticmethod # doesn't depend on the class or it's instance
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def validate_number_of_columns(self, dataFrame:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"DataFrame has columns:{dataFrame.columns}")

            if len(dataFrame.columns) == number_of_columns:
                return True
            else:
                return False
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def validate_numerical_columns(self, dataFrame:pd.DataFrame)->bool:
        try:
            
            numerical_columns = self._schema_config['numerical_columns']
            number_of_columns = len(numerical_columns)
            logging.info(f"Required number of numerical columns:{number_of_columns}")

            li = list(map(lambda x : False if x not in dataFrame.columns else True, numerical_columns))

            if False in li:
                return False
            else:
                return True
            
            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def detect_dataset_drift(self, base_df, current_df, threshold=0.05)->bool:
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1_series = base_df[column]
                d2_series = current_df[column]
                is_sample_dist = ks_2samp(d1_series, d2_series)
                
                if is_sample_dist.pvalue <= threshold:
                    is_found = True
                    status = False
                else:
                    is_found = False
                
                report.update({column:{
                    "p_value":float(is_sample_dist.pvalue),
                    "drift_status":is_found
                }})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            dir_path = os.path.dirname(drift_report_file_path)

            os.makedirs(dir_path, exist_ok=True)

            write_yaml_file(file_path = drift_report_file_path, content = report)
            

        except Exception as e:
            raise NetworkSecurityException(e, sys)
                


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## read the data from train and test
            train_dataFrame = DataValidation.read_data(train_file_path)
            test_dataFrame = DataValidation.read_data(test_file_path)

            status = self.validate_number_of_columns(dataFrame=train_dataFrame)
            if not status:
                error_message = f"Train DataFrame does not contain all the columns."

            status = self.validate_number_of_columns(dataFrame=test_dataFrame)
            if not status:
                error_message = f"Test DataFrame does not contain all the columns."
            
            status = self.validate_numerical_columns(dataFrame=train_dataFrame)
            if not status:
                error_message = f"DataFrame does not contain all the numerical columns."
            
            status = self.validate_numerical_columns(dataFrame=test_dataFrame)
            if not status:
                error_message = f"DataFrame does not contain all the numerical columns."
            

            self.detect_dataset_drift(base_df=train_dataFrame, current_df=test_dataFrame)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_dataFrame.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_dataFrame.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status, 
                valid_train_file_path = self.data_validation_config.valid_train_file_path, 
                valid_test_file_path = self.data_validation_config.valid_train_file_path, 
                invalid_train_file_path = None, 
                invalid_test_file_path = None, 
                drift_report_file_path = self.data_validation_config.drift_report_file_path)

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
                