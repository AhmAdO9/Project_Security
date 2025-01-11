import os
import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.artifact_entity import DataIngestionArtifact

from networksecurity.entity.config_entity import (
                    DataIngestionConfig,
                    TrainingPipelineConfig, 
                    DataValidationConfig, 
                    DataTransformationConfig, 
                    ModelTrainerConfig)



class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()

    
    def start_data_ingestion(self):
        try:
            logging.info("Initiate Data Ingestion")
            data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)

            dataIngestion = DataIngestion(data_ingestion_config)
            

            self.dataIngestionArtifact = dataIngestion.initiate_data_ingestion()
            logging.info("Data Ingestion Completed")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    
    def start_data_validation(self):
        try:
            logging.info("Initiate Data Validation")
            dataValidationConfig = DataValidationConfig(self.training_pipeline_config)

            dataValidation = DataValidation(dataValidationConfig, self.dataIngestionArtifact, )

            self.dataValidationArtifact = dataValidation.initiate_data_validation()
            logging.info("Data Validation Completed")

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def start_data_transformation(self):
        try:
            logging.info("Initiate Data Transformation")
            dataTransformationConfig = DataTransformationConfig(self.training_pipeline_config)

            dataTransformation = DataTransformation(dataTransformationConfig, self.dataValidationArtifact)

            self.dataTransformationArtifact = dataTransformation.initiate_data_transformation()
            logging.info("Data Transformation Completed")

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def start_model_training(self):
        try:
            logging.info("Initiate Model Training")
            modelTrainerConfig = ModelTrainerConfig(self.training_pipeline_config)

            modelTrainer = ModelTrainer(modelTrainerConfig, self.dataTransformationArtifact)

            self.modelTrainerArtifact = modelTrainer.initiate_model_trainer()
            logging.info("Model Training Completed")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    
    def run_pipeline(self):
        try:
            self.start_data_ingestion()
            self.start_data_validation()
            self.start_data_transformation()
            self.start_model_training()
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__=="__main__":
    trainingPipeline = TrainingPipeline()
    trainingPipeline.run_pipeline()