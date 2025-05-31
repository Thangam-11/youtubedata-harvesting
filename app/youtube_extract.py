import pandas as pd
import json
import isodate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config.config import get_youtube_api_key
from app.mongodb_handler import MongoDBHandler


class YouTubeExtract:

    def __init__(self):
        api_key = get_youtube_api_key()
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def channel(self, channel_id):
        request = self.youtube.channels().list(
            part='contentDetails,snippet,statistics,status',
            id=channel_id
        )
        response = request.execute()

        item = response['items'][0]

        return {
            'channel_name': item['snippet']['title'],
            'channel_id': item['id'],
            'subscription_count': item['statistics']['subscriberCount'],
            'channel_views': item['statistics']['viewCount'],
            'channel_description': item['snippet']['description'],
            'upload_id': item['contentDetails']['relatedPlaylists']['uploads'],
            'country': item['snippet'].get('country', 'Not Available')
        }

    def playlist(self, channel_id, upload_id):
        playlist = []
        next_page_token = None

        while True:
            request = self.youtube.playlists().list(
                part="snippet,contentDetails,status",
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                playlist.append({
                    'playlist_id': item['id'],
                    'playlist_name': item['snippet']['title'],
                    'channel_id': channel_id,
                    'upload_id': upload_id
                })

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        return playlist

    def video_ids(self, upload_id):
        video_ids = []
        next_page_token = None

        while True:
            request = self.youtube.playlistItems().list(
                part='contentDetails',
                playlistId=upload_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                video_ids.append(item['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        return video_ids

    def video(self, video_id, upload_id):
        def time_duration(t):
            try:
                return str(isodate.parse_duration(t))
            except Exception:
                return "Unknown"

        request = self.youtube.videos().list(
            part='contentDetails,snippet,statistics',
            id=video_id
        )
        response = request.execute()
        item = response['items'][0]

        caption_status = {'true': 'Available', 'false': 'Not Available'}

        data = {
            'video_id': item['id'],
            'video_name': item['snippet']['title'],
            'video_description': item['snippet']['description'],
            'upload_id': upload_id,
            'published_date': item['snippet']['publishedAt'][0:10],
            'published_time': item['snippet']['publishedAt'][11:19],
            'view_count': item['statistics']['viewCount'],
            'like_count': item['statistics'].get('likeCount', 0),
            'favourite_count': item['statistics']['favoriteCount'],
            'comment_count': item['statistics'].get('commentCount', 0),
            'duration': time_duration(item['contentDetails']['duration']),
            'thumbnail': item['snippet']['thumbnails']['default']['url'],
            'caption_status': caption_status.get(item['contentDetails']['caption'], 'Not Available')
        }

        tags = item['snippet'].get('tags')
        if tags:
            data['tags'] = tags

        return data

    def comment(self, video_id):
        comments = []
        try:
            request = self.youtube.commentThreads().list(
                part='id,snippet',
                videoId=video_id,
                maxResults=100,
                textFormat="plainText"
            )
            response = request.execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'comment_id': item['id'],
                    'comment_text': comment['textDisplay'],
                    'comment_author': comment['authorDisplayName'],
                    'comment_published_date': comment['publishedAt'][0:10],
                    'comment_published_time': comment['publishedAt'][11:19],
                    'video_id': video_id
                })

        except HttpError as e:
            error_response = json.loads(e.content.decode())
            error_reason = error_response["error"]["errors"][0].get("reason", "")
            if error_reason != "commentsDisabled":
                print(f"Error fetching comments for {video_id}: {e}")
            # If comments are disabled, silently skip.

        return comments

    def main(self, channel_id):
        channel = self.channel(channel_id)
        upload_id = channel['upload_id']
        playlists = self.playlist(channel_id, upload_id)
        video_ids = self.video_ids(upload_id)

        videos = []
        comments = []

        for vid in video_ids:
            video_data = self.video(vid, upload_id)
            videos.append(video_data)

            comment_data = self.comment(vid)
            if comment_data:
                comments.extend(comment_data)

        return {
            'channel': channel,
            'playlist': playlists,
            'video': videos,
            'comment': comments
        }

    def display_sample_data(self, channel_id):
        channel = self.channel(channel_id)
        upload_id = channel['upload_id']
        playlists = self.playlist(channel_id, upload_id)
        video_ids = self.video_ids(upload_id)

        videos = []
        comments = []

        if video_ids:
            video_data = self.video(video_ids[0], upload_id)
            videos.append(video_data)

            comment_data = self.comment(video_ids[0])
            if comment_data:
                comments.extend(comment_data)

        return {
            'channel': channel,
            'playlist': playlists,
            'video': videos,
            'comment': comments

        }
 