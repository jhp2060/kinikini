from .base import *

DEBUG = False

ALLOWED_HOSTS = secrets['ALLOWED_HOST']

DATABASES = {
    'default' : secrets['DB_SETTINGS']['PRODUCTION']
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITE_LIST = [
    'localhost:8000',
]