from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'yummy',
        'USER': 'root',
        'PASSWORD': '1234',
        'PORT': 5432,
    }
}