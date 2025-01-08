import os
import sys
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e


    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    
    def insert_data_to_mongodb(self, records, database, collection):
        try:
            
            self.database = database
            self.collection = collection
            self.records = records
            self.mongoclient = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongoclient[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)


        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        


if __name__=="__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "FaheemAI"
    COLLECTION = "NetworkData"
    
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    networkobj.insert_data_to_mongodb(records, DATABASE, COLLECTION)
    