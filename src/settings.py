# settings.py
from dotenv import load_dotenv
import os

load_dotenv()

TRANSLATOR_TEXT_SUBSCRIPTION_KEY = os.getenv('TRANSLATOR_TEXT_SUBSCRIPTION_KEY')
TRANSLATOR_TEXT_ENDPOINTS = os.getenv('TRANSLATOR_TEXT_ENDPOINT')
MODEL_DIR = 'models'
MODEL_NAME = '1558M'