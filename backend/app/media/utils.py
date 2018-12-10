import base64
import os
from io import BytesIO
from uuid import uuid4

from django.conf import settings

import boto3
from PIL import Image


def create_hash():
    return uuid4().hex


def create_filename(filename):
    filename, ext = filename.rsplit('.')
    return f'{filename}_{create_hash()}.{ext}'


def process_image(image_data, max_size):
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    resize_image(image=image, size=max_size)
    return image


def resize_image(image, size):
    x, y = image.size
    if x >= y:
        if x > size:
            image.thumbnail((size, int(size * y / x)), Image.ANTIALIAS)
    else:
        if y > size:
            image.thumbnail((int(size * x / y), size), Image.ANTIALIAS)


def upload_file_to_s3(file, filename, acl="public-read"):
    extension_to_content_type = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'gif': 'image/gif'
    }

    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.UPLOAD_APP['s3']['AWS_ACCESS_KEY'],
        aws_secret_access_key=settings.UPLOAD_APP['s3']['AWS_SECRET_KEY'],
        region_name=settings.UPLOAD_APP['s3']['S3_REGION_NAME'],
    )
    bucket_name = settings.UPLOAD_APP['s3']['S3_BUCKET_NAME']
    ext = filename.rsplit('.', 1)[-1]
    key_name = os.path.join(settings.UPLOAD_APP['s3']['S3_BUCKET_FOLDER'], filename)

    if ext in extension_to_content_type.keys():
        content_type = extension_to_content_type[ext]
    else:
        content_type = "application/octet-stream"

    s3.upload_fileobj(
        file,
        bucket_name,
        key_name,
        ExtraArgs={
            "ACL": acl,
            "ContentType": content_type,
            'Cache-Control': f"max-age={settings.UPLOAD_APP['s3']['S3_MAX_AGE']},public"
        }
    )
