from os import path
from django.conf import settings
from abc import ABCMeta
from .tasks import local_upload

FORMAT_EXT_MAP = {'JPEG': '.jpg',
                  'JPEG 200': '.jpg',
                  'PNG': '.png',
                  'GIF': '.gif'}


class AbstractUploadStrategy(metaclass=ABCMeta):
    task = NotImplemented

    def __init__(self, filename, image, max_size):
        self.filename = filename
        self.image = image
        self.max_size = max_size

    def get_url(self):
        raise NotImplemented

    @property
    def url(self):
        return self.get_url()

    def execute(self):
        self.task.apply_async(args=[self.filename, self.image, self.max_size])


class LocalUploadStrategy(AbstractUploadStrategy):
    task = local_upload

    def get_url(self):
        return path.join(settings.MEDIA_URL, self.filename)


class S3UploadStrategy(AbstractUploadStrategy):
    pass


STRATEGY_MAP = {
    '1': S3UploadStrategy,
    '0': LocalUploadStrategy
}


def get_upload_strategy(backend):
    return STRATEGY_MAP[backend]
