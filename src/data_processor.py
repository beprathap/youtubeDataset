import json

def extract_required_fields(raw_data):
    extracted_data = []

    # Check if raw_data is a list or a dictionary
    if isinstance(raw_data, list):
        items = raw_data
    elif isinstance(raw_data, dict) and 'items' in raw_data:
        items = raw_data['items']
    else:
        raise ValueError("Unexpected data structure in raw_data")

    for item in items:
        channel_data = {
            'channel_id': item['id'],
            'channel_title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'published_at': item['snippet']['publishedAt'],
            # 'country': item['snippet']['country'],
            'subscriber_count': item['statistics']['subscriberCount'],
            'view_count': item['statistics']['viewCount'],
            'video_count': item['statistics']['videoCount'],
            # 'last_updated':
        }
        extracted_data.append(channel_data)
    return extracted_data