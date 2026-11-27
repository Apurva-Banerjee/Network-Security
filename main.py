import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Starting data ingestion process...")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion process completed successfully.")
        print(
                    f"Data ingestion completed successfully. "
                    f"Train file path: {dataingestionartifact.train_file_path}, "
                    f"Test file path: {dataingestionartifact.test_file_path}"
                )
        data_validation_config = DataValidationConfig(training_pipeline_config)
        
        data_validation = DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Starting data validation process...")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation process completed successfully.")
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        logging.info("Starting data transformation process...")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation process completed successfully.")
        print(data_transformation_artifact)
                
       
    except Exception as e:
        raise NetworkSecurityException(e, sys)