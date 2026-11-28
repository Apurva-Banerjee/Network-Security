from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME


import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkModel:
    def __init__(self, preprocessor, model):
        """
        Initializes the NetworkModel with a preprocessor and a model.
        
        Args:
            preprocessor: The preprocessing object (e.g., scaler, encoder).
            model: The machine learning model.
        """
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
    def predict(self, X):
        """
        Predicts the output for the given input data.
        
        Args:
            X: The input data for prediction.
        Returns:

            The predicted output.
        """
        try:
            X_transformed = self.preprocessor.transform(X)
            y_hat = self.model.predict(X_transformed)
            return y_hat
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
