
# app/mongo_db.py
from pymongo import MongoClient
from config.config import get_mongo_db_uri  # Make sure this import matches your file structure

class MongoDBHandler:
    def __init__(self, db_name="youtube_analytics"):
        self.client = MongoClient(get_mongo_db_uri())
        self.db = self.client[db_name]

    def insert_one(self, collection_name, data):
        collection = self.db[collection_name]
        return collection.insert_one(data)

    def insert_many(self, collection_name, data_list):
        collection = self.db[collection_name]
        return collection.insert_many(data_list)

    def find_all(self, collection_name):
        collection = self.db[collection_name]
        return list(collection.find())
