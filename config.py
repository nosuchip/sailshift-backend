import os
from dotenv import load_dotenv

load_dotenv()

# mandatory
APP_SECRET_KEY = os.environ['APP_SECRET_KEY']
DATABASE_URI = os.environ['DATABASE_URI']
JWT_KEY = os.environ['JWT_KEY']
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
EMAIL_FROM_ADDRESS = os.environ['EMAIL_FROM_ADDRESS']
SITE_URL = os.environ['SITE_ENV']

# optionas
AUTH_TOKEN_TYPE = os.getenv('AUTH_TOKEN_TYPE', 'Bearer')

# app-specific
DATE_FORMAT_STRING = '%Y-%m-%d %H:%M:%S'


print(f'config:APP_SECRET_KEY = {APP_SECRET_KEY}')
print(f'config:DATABASE_URI = {DATABASE_URI}')
print(f'config:JWT_KEY = {JWT_KEY}')
print(f'config:SENDGRID_API_KEY = {SENDGRID_API_KEY}')
print(f'config:EMAIL_FROM_ADDRESS = {EMAIL_FROM_ADDRESS}')
print(f'config:SITE_URL = {SITE_URL}')
print(f'config:AUTH_TOKEN_TYPE = {AUTH_TOKEN_TYPE}')
print(f'config:DATE_FORMAT_STRING = {DATE_FORMAT_STRING}')


def get_url(url_key, *parts):
    urls = {
        'verify': '/accounts/verify/',
    }

    return SITE_URL + urls[url_key] + '/'.join([str(i) for i in parts])
