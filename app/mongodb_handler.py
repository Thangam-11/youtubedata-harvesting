from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDBHandler:
    def __init__(self, db_name="youtube_data"):
        mongo_uri = os.getenv("MONGO_DB_URI")
        if not mongo_uri:
            raise ValueError("MONGO_DB_URI not found in environment variables.")
        
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def find_documents(self, collection_name, query={}):
        collection = self.db[collection_name]
        return list(collection.find(query))
