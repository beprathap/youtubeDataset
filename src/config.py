import os
from dotenv import load_dotenv

load_dotenv()

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_IDS = ['UClFSU9_bUb4Rc6OYfTt5SPw', # Ask Me Anything: Philip DeFranco Showw
                'UCX6OQ3DkcsbYNE6H8uQQuVA', # Challenge: MrBeast
                'UCsooa4yRKGN_zEE8iknghZA', # Educational: Ted-Ed
                'UCh9IfI45mmk59eDvSWtuuhQ', # Funny Videos/Comedy: Ryan George
                'UCBJycsmduvYEL83R_U4JriQ', # Product Demo/Launch: MKBHD
                'UC4rlAVgAK0SGk-yTfe48Qpw', # Knowledge: BRIGHT SIDE
                'UC0v-tlzsn0QZwJnkiaUSJVQ', # Reaction Videos: React
                'UCzQUP1qoWDoEbmsQxvdjxgQ', # Video Podcasts: PowerfulJRE
                'UCoYATiiqNT7csPFqtWWfc5w', # Video Tutorials: Skillshare
                'UC-lHJZR3Gqxm24_Vd_AJ5Yw', # Gaming: PewDiePie
                'UCq-Fj5jknLsUf-MWSy4_brA' # Music: T-Series
               ]
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw')