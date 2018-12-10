from settings.common import *  # flake8:noqa
from settings.local import *
from settings.upload_settings import *  # flake8:noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

UNIT_TESTING = True
