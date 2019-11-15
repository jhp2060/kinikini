from .base import *

DEBUG = False

ALLOWED_HOSTS = secrets['ALLOWED_HOST']

DATABASES = {
    'default' : secrets['DB_SETTINGS']['PRODUCTION']
}