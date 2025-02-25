import os

from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("SECRET")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID")
APP_ID = os.getenv("APP_ID")
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
REDIS_HOST = os.getenv('REDIS_HOST')