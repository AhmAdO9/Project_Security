from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.components.data_transformation import DataTransformation


if __name__=="__main__":
    trainingPipelineConfig = TrainingPipelineConfig()
    dataIngestionConfig = DataIngestionConfig(trainingPipelineConfig)
    dataIngestion = DataIngestion(dataIngestionConfig)
    logging.info("initiate the data ingestion")
    dataIngestionArtifact = dataIngestion.initiate_data_ingestion()
    logging.info("Data initiation completed")
    print(dataIngestionArtifact)
    print('\n')
    logging.info('Data Validation begins')
    data_validation_config = DataValidationConfig(trainingPipelineConfig)
    data_validation = DataValidation(data_validation_config, dataIngestionArtifact)
    data_validation_artifact = data_validation.initiate_data_validation()
    print(data_validation_artifact)
    logging.info("Data Validation completed")
    print('\n')
    data_transformation_config = DataTransformationConfig(trainingPipelineConfig)
    data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
    data_transformation_artifact = data_transformation.initiate_data_transformation()
    print(data_transformation_artifact)
    logging.info("Data Transformation completed")






