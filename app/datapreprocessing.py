from googleapiclient.discovery import build
from config.config import get_youtube_api_key  # Your method to fetch API key

def get_channel_id_by_handle(handle):
    api_key = get_youtube_api_key()
    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        q=handle,
        type="channel",
        part="snippet,id",
        maxResults=1
    )
    response = request.execute()

    if response["items"]:
        channel_id = response["items"][0]["id"]["channelId"]  # ✅ FIXED
        print(f"Channel ID for {handle} is: {channel_id}")
        return channel_id
    else:
        raise ValueError(f"No channel found for handle: {handle}")

# Example usage
if __name__ == "__main__":
    get_channel_id_by_handle("@codebasics")
