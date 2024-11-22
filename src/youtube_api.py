import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class YouTubeAPI:
    def __init__(self, api_key):
        # Builds a new instance of YouTube.
        self.youtube = build('youtube', 'v3', developerKey=api_key)

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

    # This method saves the raw JSON data into a file
    def save_raw_json(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f)
# Add more methods for other API calls (e.g., get_video_stats, get_comments)