import os
from dotenv import load_dotenv

load_dotenv()

BASE_FOLDERS_NAMES = ["db"]
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CHANNEL_DONOR = int(os.getenv('CHANNEL_DONOR'))
CHANNEL_RECIPIENT = os.getenv('CHANNEL_RECIPIENT')

POST_IN_DAY = 16
POST_IN_ONE_TIME = 8
MORNING_POST_TIME = '07:15'
NIGHT_POST_TIME = '19:20'

# set time on Linux Server:
# date
# timedatectl
# sudo timedatectl set-timezone Asia/Atyrau
