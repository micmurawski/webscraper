from os import path

from django.conf import settings

from settings.celery import app  # flake8:noqa

from .utils import process_image, upload_file_to_s3


@app.task(ignore_result=True)
def local_upload(filename, image, max_size, *args, **kwargs):
    pil_img = process_image(image, max_size)
    file_path = path.join(settings.MEDIA_ROOT, filename)
    pil_img.save(fp=file_path)


@app.task(ignore_result=True)
def s3_upload(filename, image, max_size, *args, **kwargs):
    pil_img = process_image(image, max_size)
    upload_file_to_s3(pil_img, filename)
