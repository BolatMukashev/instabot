import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = bool(int(os.getenv('DEBUG')))

BASE_FOLDERS_NAMES = ["db"]
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_TOKEN_TEST = os.getenv('BOT_TOKEN_TEST')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CHANNEL_DONOR = int(os.getenv('CHANNEL_DONOR'))
CHANNEL_RECIPIENT = os.getenv('CHANNEL_RECIPIENT')
CHANNEL_RECIPIENT_TEST = os.getenv('CHANNEL_RECIPIENT_TEST')

POST_IN_DAY = int(os.getenv('POST_IN_DAY'))
POST_IN_ONE_TIME = int(os.getenv('POST_IN_ONE_TIME'))
MORNING_POST_TIME = os.getenv('MORNING_POST_TIME')
NIGHT_POST_TIME = os.getenv('NIGHT_POST_TIME')

# set time on Linux Server:
# date
# timedatectl
# sudo timedatectl set-timezone Asia/Atyrau
