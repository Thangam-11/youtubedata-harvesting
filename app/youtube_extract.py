from googleapiclient.discovery import build
from config.config import YOUTUBE_API_KEY

class youtube_extract:

    def __init__(self):
        self.youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    def get_channel_details(self, channel_id):
        request = self.youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id
        )
        response = request.execute()
        if not response["items"]:
            return None

        channel = response["items"][0]
        return {
            "channel_id": channel_id,
            "channel_name": channel["snippet"]["title"],
            "description": channel["snippet"]["description"],
            "published_at": channel["snippet"]["publishedAt"],
            "subscribers": int(channel["statistics"].get("subscriberCount", 0)),
            "views": int(channel["statistics"].get("viewCount", 0)),
            "total_videos": int(channel["statistics"].get("videoCount", 0)),
            "playlist_id": channel["contentDetails"]["relatedPlaylists"]["uploads"]
        }

    def get_videos_from_playlist(self, playlist_id):
        videos = []
        next_page_token = None

        while True:
            request = self.youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            for item in response["items"]:
                videos.append({
                    "video_id": item["snippet"]["resourceId"]["videoId"],
                    "title": item["snippet"]["title"],
                    "published_at": item["snippet"]["publishedAt"]
                })
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        return videos

    def get_video_details(self, video_ids):
        video_details = []
        for i in range(0, len(video_ids), 50):
            request = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=",".join(video_ids[i:i+50])
            )
            response = request.execute()
            for item in response["items"]:
                video_details.append({
                    "video_id": item["id"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "tags": item["snippet"].get("tags", []),
                    "views": int(item["statistics"].get("viewCount", 0)),
                    "likes": int(item["statistics"].get("likeCount", 0)),
                    "comments": int(item["statistics"].get("commentCount", 0)),
                    "duration": item["contentDetails"]["duration"]
                })
        return video_details

    def get_comments(self, video_id):
        comments = []
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=20,
                textFormat="plainText"
            )
            response = request.execute()
            for item in response["items"]:
                top_comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "video_id": video_id,
                    "author": top_comment["authorDisplayName"],
                    "comment": top_comment["textDisplay"],
                    "likes": top_comment["likeCount"],
                    "published_at": top_comment["publishedAt"]
                })
        except Exception as e:
            print(f"Error fetching comments for {video_id}: {e}")
        return comments

    def main(self, channel_id):
        channel_info = self.get_channel_details(channel_id)
        if not channel_info:
            return {"error": "Channel not found"}

        videos_raw = self.get_videos_from_playlist(channel_info["playlist_id"])
        video_ids = [v["video_id"] for v in videos_raw]
        video_details = self.get_video_details(video_ids)

        all_comments = []
        for vid in video_ids:
            comments = self.get_comments(vid)
            all_comments.extend(comments)

        return {
            "channel": channel_info,
            "videos": video_details,
            "comments": all_comments
        }


# For quick test
if __name__ == "__main__":
    yt = youtube_extract()
    data = yt.main("UC_x5XG1OV2P6uZZ5FSM9Ttw")  # Replace with any valid channel ID
    from pprint import pprint
    pprint(data)
