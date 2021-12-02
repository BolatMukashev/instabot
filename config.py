import os
from dotenv import load_dotenv

load_dotenv()

BASE_FOLDERS_NAMES = ["db"]
INST_USERNAME = os.getenv('INST_USERNAME')
INST_PASSWORD = os.getenv('INST_PASSWORD')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CHANNEL_DONOR = int(os.getenv('CHANNEL_DONOR'))
CHANNEL_RECIPIENT = os.getenv('CHANNEL_RECIPIENT')
CHANNEL_ADDRESS = os.getenv('CHANNEL_ADDRESS')
BOT_TOKEN = os.getenv('BOT_TOKEN')
POST_IN_DAY = 16
POST_IN_ONE_TIME = 8
PHOTO_SAVE_FOLDER_NAME = 'photos'
MORNING_POST_TIME = '7:20'
NIGHT_POST_TIME = '19:20'
PHOTO_DB_UPDATE_TIME = '5:00'

# set time on Linux Server:
# date
# timedatectl
# sudo timedatectl set-timezone Asia/Atyrau