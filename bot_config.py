import os
from dotenv import load_dotenv

load_dotenv()

BASE_FOLDER_NAMES = ["db", "photos"]
INST_USERNAME = os.getenv('INST_USERNAME')
INST_PASSWORD = os.getenv('INST_PASSWORD')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CHAT_NAME = os.getenv('CHAT_NAME')
BOT_TOKEN = os.getenv('BOT_TOKEN')
POST_IN_DAY = 20
POST_IN_ONE_TIME = 10
PHOTO_SAVE_FOLDER_NAME = 'photos'
TIME_TO_SLEEP = 5
DOWNLOAD_START_WITH = 0
