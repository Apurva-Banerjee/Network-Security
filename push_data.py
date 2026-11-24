import os
import sys
import json
import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
CA_BUNDLE = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            if not MONGO_DB_URL:
                raise ValueError("MONGO_DB_URL is not set in the environment variables.")
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=CA_BUNDLE)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def csv_to_json_converter(self, file_path: str) -> list[dict]:
        try:
            logging.info(f"Reading CSV file from: {file_path}")
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            logging.info(f"Converted {len(records)} rows to JSON records.")
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def insert_data_mongodb(self, records: list[dict], database: str, collection: str) -> int:
        try:
            db = self.mongo_client[database]
            col = db[collection]
            result = col.insert_many(records)
            inserted_count = len(result.inserted_ids)
            logging.info(f"Inserted {inserted_count} records into {database}.{collection}.")
            return inserted_count
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e


if __name__ == "__main__":
    FILE_PATH = os.path.join("Network_Data", "phisingData.csv")
    DATABASE = "NetworkSecurity"
    COLLECTION = "NetworkData"

    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_converter(FILE_PATH)
    no_of_records = network_obj.insert_data_mongodb(records, DATABASE, COLLECTION)
    print(f"Number of records inserted into MongoDB: {no_of_records}")