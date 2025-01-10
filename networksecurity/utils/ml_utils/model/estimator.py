import os, sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import(
                MODEL_TRAINER_DIR_NAME, 
                MODEL_TRAINER_TRAINED_MODEL_DIR, 
                MODEL_TRAINER_TRAINED_MODEL_NAME)



class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
      
        except Exception as e:
            raise NetworkSecurityException(e, sys)

        
    def predict(self, data):
        try:
           transformed_data = self.preprocessor.transform(data)
           y_pred = self.model.predict(transformed_data)
          
           return y_pred
       
        except Exception as e:
            raise NetworkSecurityException(e, sys)