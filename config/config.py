from dotenv import load_dotenv
import os

def get_youtube_api_key():
    """
    Load the environment variables from a .env file and return the YOUTUBE_API_KEY.
    
    Returns:
        str: The YouTube API key from environment variables.
    """
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY not found in environment variables.")
    return api_key
def get_mongo_db_uri():
    """
    Load the environment variables from a .env file and return the MONGO_DB_URI.
    
    Returns:
        str: The MongoDB URI from environment variables.
    """
    load_dotenv()
    mongo_uri = os.getenv("MONGO_DB_URI")
    
    if not mongo_uri:
        raise ValueError("MONGO_DB_URI not found in environment variables.")
    return mongo_uri
