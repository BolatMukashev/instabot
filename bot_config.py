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
HASH_JSON_FILE_NAME = 'all_images_hashes.json'
JSON_FILE_WITH_NICKNAMES = 'nicknames.json'
