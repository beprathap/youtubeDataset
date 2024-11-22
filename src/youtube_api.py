import os
import json
from datetime import datetime, timedelta

import googleapiclient
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeAPI:
    SCOPES = ['https://www.googleapis.com/auth/youtube.readonly',
              'https://www.googleapis.com/auth/yt-analytics.readonly']

    def __init__(self, api_key, credentials_file):
        # Builds a new instance of YouTube.
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.youtube_analytics = None
        self.authenticate(credentials_file)

    def authenticate(self, credentials_file):
        # Define the scopes for YouTube Data API and YouTube Analytics API
        SCOPES = [
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/yt-analytics.readonly"
        ]

        # Check if token.json exists for storing access tokens
        if os.path.exists('config/token.json'):
            creds = Credentials.from_authorized_user_file('config/token.json', self.SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, self.SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for future use
            with open('config/token.json', 'w') as token:
                token.write(creds.to_json())

        # Build the YouTube and YouTube Analytics service objects
        self.youtube_analytics = build('youtubeAnalytics', 'v2', credentials=creds)

    def get_channel_stats(self, channel_ids):
        try:
            request = self.youtube.channels().list(
                part='snippet, contentDetails, statistics',
                id=','.join(channel_ids)
            )
            response = request.execute()
            return response['items']
        except HttpError as e:
            print(f'An error occured: {e}')
            return None

    def get_latest_videos(self, channel_id, max_results=10):
        try:
            request = self.youtube.search().list(
                part='id, snippet',
                channelId=channel_id,
                type='video',
                order='date',
                maxResults=max_results
            )
            response = request.execute()
            video_ids = [item['id']['videoId'] for item in response['items']]
            return self.get_video_details(video_ids)
        except HttpError as e:
            print(f'An error occurred: {e}')
            return None

    def get_video_details(self, video_ids):
        try:
            request = self.youtube.videos().list(
                part='snippet, contentDetails, statistics',
                id=','.join(video_ids)
            )
            response = request.execute()
            return response['items']
        except HttpError as e:
            print(f'An error occurred: {e}')
            return None


    def get_video_comments(self, video_id, max_results=50):
        try:
            request = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=max_results
            )
            response = request.execute()
            return response['items']
        except HttpError as e:
            print(f'An error occurred: {e}')
            return None

    def get_daily_stats(self, video_ids, days=28):
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)

            daily_stats = []

            for video_id in video_ids:
                # Get video details to retrieve channel_id
                video_details = self.get_video_details([video_id])
                if not video_details:
                    continue  # Skip if no details found

                channel_id = video_details[0]['snippet']['channelId']

                # Query the YouTube Analytics API for daily stats
                request = self.youtube_analytics.reports().query(
                    ids=f'channel=={channel_id}',
                    startDate=start_date.isoformat(),
                    endDate=end_date.isoformat(),
                    metrics='views,likes,dislikes,comments',
                    dimensions='day',
                    filters=f'video=={video_id}'
                )
                response = request.execute()

                for row in response.get('rows', []):
                    date, views, likes, dislikes, comments = row
                    daily_stats.append({
                        'date': date,
                        'channel_id': channel_id,
                        'video_id': video_id,
                        'view_count': int(views),
                        'like_count': int(likes),
                        'dislike_count': int(dislikes),
                        'comment_count': int(comments)
                    })

            return daily_stats
        except HttpError as e:
            print(f'An error occurred: {e}')
            return None

    def get_video_categories(self, video_ids):
        try:
            categories = {}
            for video_id in video_ids:
                request = self.youtube.videos().list(
                    part='snippet',
                    id=video_id
                )
                response = request.execute()
                if 'items' in response and len(response['items']) > 0:
                    category_id = response['items'][0]['snippet']['categoryId']
                    category_request = self.youtube.videoCategories().list(
                        part='snippet',
                        id=category_id
                    )
                    category_response = category_request.execute()
                    if 'items' in category_response and len(category_response['items']) > 0:
                        category_title = category_response['items'][0]['snippet']['title']
                        categories[video_id] = {
                            'category_id': int(category_id),
                            'title': category_title
                        }
            return categories
        except HttpError as e:
            print(f'An error occurred: {e}')
            return None

    # Add more methods for other API calls (e.g., get_video_stats, get_comments)
    # This method saves the raw JSON data into a file
    def save_raw_json(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)