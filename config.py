import os
from dotenv import load_dotenv

load_dotenv()

APP_SECRET_KEY = os.environ['APP_SECRET_KEY']
DATABASE_URI = os.environ['DATABASE_URI']
JWT_KEY = os.environ['JWT_KEY']

DATE_FORMAT_STRING = '%Y-%m-%d %H:%M:%S'
