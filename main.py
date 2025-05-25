from app.youtube_extract import YouTubeExtract
from config.config import get_youtube_api_key

# Optional: Get channel ID from handle (like @codebasics)
def get_channel_id_by_handle(handle):
    from googleapiclient.discovery import build

    api_key = get_youtube_api_key()
    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        q=handle,
        type="channel",
        part="snippet",
        maxResults=1
    )
    response = request.execute()

    if response["items"]:
        return response["items"][0]["snippet"]["channelId"]
    else:
        raise ValueError(f"No channel found for handle: {handle}")

if __name__ == "__main__":
    try:
        handle = "UCZLJf_R2sWyUtXSKiKlyvAw"  # or use actual channel ID like "UCZLJf_R2sWyUtXSKiKlyvAw"
        channel_id = get_channel_id_by_handle(handle)
        
        yt = YouTubeExtract()
        result = yt.display_sample_data(channel_id)
        
        import json
        print(json.dumps(result, indent=4))
        print("\n✅ Test successful: `YouTubeExtract` is working.")
    except Exception as e:
        print("❌ Test failed with error:")
        print(e)
