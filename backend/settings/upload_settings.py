import os

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY', None)
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY', None)
BASE_URL = os.environ.get('S3_BASE_URL', 's3.amazonaws.com/')
S3_REGION_NAME = os.environ.get('S3_REGION_NAME', 'eu-west-2')
S3_MAX_AGE = os.environ.get('S3_MAX_AGE', '31536000')
S3_BUCKET_FOLDER = os.environ.get('S3_BUCKET_FOLDER', 'images')

DEFAULT_MAX_SIZE = os.environ.get('DEFAULT_MAX_SIZE', 1000)

UPLOAD_APP = {
    'local': {
        'DEFAULT_MAX_SIZE': DEFAULT_MAX_SIZE,
    },
    's3': {
        'AWS_ACCESS_KEY': AWS_ACCESS_KEY,
        'AWS_SECRET_KEY': AWS_SECRET_KEY,
        'S3_REGION_NAME': S3_REGION_NAME,
        'S3_MAX_AGE': S3_MAX_AGE,
        'S3_BUCKET_FOLDER': S3_BUCKET_FOLDER,
        'DEFAULT_MAX_SIZE': DEFAULT_MAX_SIZE,
        'BASE_URL': BASE_URL
    }
}
