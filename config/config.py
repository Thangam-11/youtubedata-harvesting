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
