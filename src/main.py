import os # For file and path operations
from datetime import datetime
from src.config import API_KEY, CHANNEL_IDS, RAW_DATA_PATH, PROCESSED_DATA_PATH
from src.youtube_api import YouTubeAPI
from src.data_processor import extract_required_fields
from src.data_transformer import update_datatypes, save_to_csv

def main():
    # Initialize YouTube API
    api = YouTubeAPI(API_KEY)

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Extract and save raw JSON
    raw_data = api.get_channel_stats(CHANNEL_IDS)
    if raw_data:
        raw_filename = os.path.join(RAW_DATA_PATH, f'youtube_raw_{timestamp}.json')
        api.save_raw_json(raw_data, raw_filename)
        print(f"Raw data saved to {raw_filename}")

        # Print raw_data structure for debugging
        print("Raw data structure:", type(raw_data))
        if isinstance(raw_data, dict):
            print("Keys in raw_data:", raw_data.keys())
        elif isinstance(raw_data, list):
            print("Number of items in raw_data:", len(raw_data))

        # Process data
        extracted_data = extract_required_fields(raw_data)

        # Transform data
        df = update_datatypes(extracted_data)

        # Save processed data
        processed_filename = os.path.join(PROCESSED_DATA_PATH, f'youtube_processed_{timestamp}.csv')
        save_to_csv(df, processed_filename)
        print(f"Processed data saved to {processed_filename}")
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    main()