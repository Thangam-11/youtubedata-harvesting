from googleapiclient.discovery import build
from config.config import get_youtube_api_key
from app.youtube_extract import YouTubeExtract  # Assuming your class is in this file

# Optional: Get channel ID from handle like "@codebasics"
def get_channel_id_by_handle(handle):
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
        # Either a handle like "@codebasics" or direct channel ID
        input_id = "@codebasics"
        
        if input_id.startswith("@"):
            channel_id = get_channel_id_by_handle(input_id)
        else:
            channel_id = input_id

        yt = YouTubeExtract()
        result = yt.display_sample_data(channel_id)

        import json
        print(json.dumps(result, indent=4))
        print("\n✅ Test successful: YouTubeExtract is working.")

    except Exception as e:
        print("❌ Test failed with error:")
        print(e)
