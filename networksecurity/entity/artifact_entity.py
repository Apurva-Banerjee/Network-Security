from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    """
    DataIngestionArtifact is a dataclass that holds information about the data ingestion process.
    It contains the following attributes:
    
    Attributes:
        train_file_path (str): The file path to the training dataset.
        test_file_path (str): The file path to the testing dataset.
        is_ingested (bool): A flag indicating whether the data ingestion was successful.
        message (str): A message providing additional information about the data ingestion process.
    """
    train_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    """
    DataValidationArtifact is a dataclass that holds information about the data validation process.
    It contains the following attributes:
    
    Attributes:
        valid_train_file_path (str): The file path to the validated training dataset.
        valid_test_file_path (str): The file path to the validated testing dataset.
        invalid_train_file_path (str): The file path to the invalid training dataset.
        invalid_test_file_path (str): The file path to the invalid testing dataset.
        drift_report_file_path (str): The file path to the drift report generated during validation.
        is_validated (bool): A flag indicating whether the data validation was successful.
        message (str): A message providing additional information about the data validation process.
    """
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
    validation_status: bool
    
    
@dataclass
class DataTransformationArtifact:
    """
    DataTransformationArtifact is a dataclass that holds information about the data transformation process.
    It contains the following attributes:
    
    Attributes:
        transformed_train_file_path (str): The file path to the transformed training dataset.
        transformed_test_file_path (str): The file path to the transformed testing dataset.
        is_transformed (bool): A flag indicating whether the data transformation was successful.
        message (str): A message providing additional information about the data transformation process.
    """
    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str
    
    
@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    precision_score: float
    recall_score: float
    
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact