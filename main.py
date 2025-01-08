from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.artifact_entity import DataIngestionArtifact

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







