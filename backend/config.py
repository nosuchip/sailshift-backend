import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = 'sailshift'

# mandatory
APP_SECRET_KEY = os.environ['APP_SECRET_KEY']
DATABASE_URI = os.environ['DATABASE_URI']
JWT_KEY = os.environ['JWT_KEY']
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
EMAIL_FROM_ADDRESS = os.environ['EMAIL_FROM_ADDRESS']
SITE_URL = os.environ['SITE_ENV']

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_REGION = os.environ['AWS_REGION']
AWS_S3_BUCKET = os.environ['AWS_S3_BUCKET']

STRIPE_API_KEY = os.environ['STRIPE_API_KEY']
STRIPE_WEBHOOK_SECRET = os.environ['STRIPE_WEBHOOK_SECRET']

# optionas
AUTH_TOKEN_TYPE = os.getenv('AUTH_TOKEN_TYPE', 'Bearer')

# app-specific
DATE_FORMAT_STRING = '%Y-%m-%d %H:%M:%S'
EXCERPTS_LINES_COUNT = 50
DOCUMENT_DOWNLOAD_EXPIRATION_TIME_SEC = 10 * 60

print(f'config:APP_SECRET_KEY = {APP_SECRET_KEY}')
print(f'config:DATABASE_URI = {DATABASE_URI}')
print(f'config:JWT_KEY = {JWT_KEY}')
print(f'config:SENDGRID_API_KEY = {SENDGRID_API_KEY}')
print(f'config:EMAIL_FROM_ADDRESS = {EMAIL_FROM_ADDRESS}')
print(f'config:SITE_URL = {SITE_URL}')
print(f'config:AWS_ACCESS_KEY_ID = {AWS_ACCESS_KEY_ID}')
print(f'config:AWS_SECRET_ACCESS_KEY = {AWS_SECRET_ACCESS_KEY}')
print(f'config:AWS_REGION = {AWS_REGION}')
print(f'config:AWS_S3_BUCKET = {AWS_S3_BUCKET}')
print(f'config:STRIPE_API_KEY = {STRIPE_API_KEY}')
print(f'config:STRIPE_WEBHOOK_SECRET = {STRIPE_WEBHOOK_SECRET}')
print(f'config:AUTH_TOKEN_TYPE = {AUTH_TOKEN_TYPE}')
print(f'config:DATE_FORMAT_STRING = {DATE_FORMAT_STRING}')
print(f'config:EXCERPTS_LINES_COUNT = {EXCERPTS_LINES_COUNT}')
print(f'config:DOCUMENT_DOWNLOAD_EXPIRATION_TIME_SEC = {DOCUMENT_DOWNLOAD_EXPIRATION_TIME_SEC}')


def get_url(url_key, *parts):
    urls = {
        'verify': '/api/accounts/verify/',  # this is an exceptional case
        'reset_password': '/account/reset_password/',
    }

    return SITE_URL + urls[url_key] + '/'.join([str(i) for i in parts])
