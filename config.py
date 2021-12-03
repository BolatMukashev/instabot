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
POST_IN_DAY = 4
POST_IN_ONE_TIME = 2
PHOTO_SAVE_FOLDER_NAME = 'photos'
MORNING_POST_TIME = '11:21'
NIGHT_POST_TIME = '11:22'

# set time on Linux Server:
# date
# timedatectl
# sudo timedatectl set-timezone Asia/Atyrau
