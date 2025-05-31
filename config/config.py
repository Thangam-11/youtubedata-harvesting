from dotenv import load_dotenv
import os

load_dotenv()

def get_youtube_api_key():
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY not found in environment variables.")
    return api_key

def get_mongo_db_uri():
    mongo_uri = os.getenv("MONGO_DB_URI")
    if not mongo_uri:
        raise ValueError("MONGO_DB_URI not found in environment variables.")
    return mongo_uri
