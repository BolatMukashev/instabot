import os
from dotenv import load_dotenv

load_dotenv()

INST_USERNAME = os.getenv('INST_USERNAME')
INST_PASSWORD = os.getenv('INST_PASSWORD')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CHAT_ID = int(os.getenv('CHAT_ID'))
