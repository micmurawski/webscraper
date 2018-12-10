import os

from settings.celery_settings import *
from settings.common import *  # flake8:noqa
from settings.local import *  # flake8:noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'app'),
        'USER': os.environ.get('DB_USER', 'app'),
        'PASSWORD': os.environ.get('DB_USER_PASSWORD', 'secret_pass'),
        'HOST': os.environ.get('DB_HOST', 'app-db'),
        'PORT': os.environ.get('DB_PORT', 5432),
        'TEST': {
            'NAME': 'test_app',
        },
        'ATOMIC_REQUESTS': True,
    }
}
