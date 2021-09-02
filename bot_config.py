import os
from dotenv import load_dotenv

load_dotenv()

BASE_FOLDERS_NAMES = ["db", "photos"]
INST_USERNAME = os.getenv('INST_USERNAME')
INST_PASSWORD = os.getenv('INST_PASSWORD')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CHANNEL_NAME = os.getenv('CHANNEL_NAME')
CHANNEL_ADDRESS = os.getenv('CHANNEL_ADDRESS')
BOT_TOKEN = os.getenv('BOT_TOKEN')
POST_IN_DAY = 20
POST_IN_ONE_TIME = 10
PHOTO_SAVE_FOLDER_NAME = 'photos'
MORNING_POST_TIME = '7:17'
NIGHT_POST_TIME = '22:10'
PHOTO_DB_UPDATE_TIME = '5:00'
