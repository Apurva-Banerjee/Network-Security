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
    