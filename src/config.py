import os
from dotenv import load_dotenv

load_dotenv()

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_IDS = ['UCX6OQ3DkcsbYNE6H8uQQuVA', #MrBeastt
              'UCq-Fj5jknLsUf-MWSy4_brA', #T-Series
              'UCbCmjCuTUZos6Inko4u57UQ', #Cocomelon-Nursery Rhymes
              'UCpEhnqL0y41EpW2TvWAHD7Q' #SET India
             ]
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw')
PROCESSED_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed')