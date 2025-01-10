import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
import pickle
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV


def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path, "rb") as file_object:
            return yaml.safe_load(file_object)

    except Exception as e:
        raise NetworkSecurityException(e, sys)


def write_yaml_file(file_path:str, content:object, replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file_object:
            return yaml.dump(content, file_object)

    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_numpy_array_data(file_path:str, array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_object:
            np.save(file_object, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_object(file_path:str, obj:object) -> None:
    try:
        logging.info("Entered the save Object method")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_object:
            pickle.dump(obj, file_object)
        logging.info("Saved the Object successfully")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file:{file_path} doesn't exist")
        with open(file_path, 'rb') as file_object:
            return pickle.load(file_object)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def load_numpy_array_data(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file:{file_path} doesn't exist")
        with open(file_path, 'rb') as file_object:
            return np.load(file_object)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def evaluate_models(x_train, x_test, y_train, y_test, models, params):
    try:
        report = {}

        for i in range(len(models)):
            model_name = list(models.items())[i][0]
            model = list(models.items())[i][1]
            param = params[list(models.keys())[i]]

            gs = GridSearchCV(model, param, cv=3)
            gs.fit(x_train, y_train)

            best_model = gs.best_estimator_
            best_model.fit(x_train, y_train)

            y_pred = best_model.predict(x_test)

            score = f1_score(y_test, y_pred)
            
            report.update({model_name:{'score':score, 'model':best_model}})

            logging.info(f"Training with {model_name} completed")
        
        logging.info(report)

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)
        