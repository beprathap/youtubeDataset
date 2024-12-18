import os # For file and path operations
from datetime import datetime
from .youtube_api import YouTubeAPI
from .config import API_KEY, CHANNEL_IDS, RAW_DATA_PATH

def airflowYoutube():
    # Initialize YouTube API
    api = YouTubeAPI(API_KEY)

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Extract and save raw JSON
    channel_stats = api.get_channel_stats(CHANNEL_IDS)

    # Extract and save channel stats
    if channel_stats:
        raw_filename = os.path.join(RAW_DATA_PATH, f'channel_stats_{timestamp}.json')
        api.save_raw_json(channel_stats, raw_filename)
        print(f"Raw data saved to {raw_filename}")
    else:
        print("Failed to retrieve data")

    # Extract and save video details for each channel
    all_video_details = []
    video_ids = [] # List to store all video IDs
    for channel_id in CHANNEL_IDS:
        latest_videos = api.get_latest_videos(channel_id)
        if latest_videos:
            print(f"Retrieved video details for channel {channel_id}")
            all_video_details.extend(latest_videos) # Add videos to the master list

            # Extract video IDs and add them to the video_ids list
            video_ids.extend([video['id'] for video in latest_videos])

    # Save all video details to a single JSON file
    if all_video_details:
        raw_filename = os.path.join(RAW_DATA_PATH, f'video_details_{timestamp}.json')
        api.save_raw_json(all_video_details, raw_filename)

    # Extract and save video comments
    all_comments = []
    for video in all_video_details:
        video_id = video['id']
        comments = api.get_video_comments(video_id)
        if comments:
            print(f"Retrieved comments for video {video_id}")
            for comment in comments:
                comment_data = {
                    'video_id': video_id,
                    'comment_id': comment['id'],
                    'author_name': comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    'text': comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                    'like_count': comment['snippet']['topLevelComment']['snippet']['likeCount'],
                    'published_at': comment['snippet']['topLevelComment']['snippet']['publishedAt']
                }
                all_comments.append(comment_data)
        else:
            print(f"Failed to retrieve comments for video {video_id}")

    # Save all comments to a single JSON file
    if all_comments:
        comment_filename = os.path.join(RAW_DATA_PATH, f'video_comments_{timestamp}.json')
        api.save_raw_json(all_comments, comment_filename)
        print(f"Video comments saved to {comment_filename}")
    else:
        print("No comments were retrieved")

    # Extract and save video/channel stats

    # Extract and save video categories
    video_categories = api.get_video_categories(video_ids)
    if video_categories:
        categories_filename = os.path.join(RAW_DATA_PATH, f'video_categories_{timestamp}.json')
        api.save_raw_json(video_categories, categories_filename)
        print(f"Video categories saved to {categories_filename}")
    else:
        print("Failed to retrieve video categories")

if __name__ == "__main__":
    airflowYoutube()