from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig


if __name__=="__main__":
    trainingPipelineConfig = TrainingPipelineConfig()
    dataIngestionConfig = DataIngestionConfig(trainingPipelineConfig)
    dataIngestion = DataIngestion(dataIngestionConfig)
    logging.info("initiate the data ingestion")
    dataIngestionArtifact = dataIngestion.initiate_data_ingestion()
    print(dataIngestionArtifact)



