import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
import pickle


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
