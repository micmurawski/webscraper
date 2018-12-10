from django.conf import settings
from django.db import models

from .core import TimestampedModel


class Task(TimestampedModel):
    GENERIC_PARSER = '0'
    PARSER_CHOICE = (
        (GENERIC_PARSER, 'GenericParser'),
    )

    GENERIC_CRAWLER = '0'
    CRAWLER_CHOICE = (
        (GENERIC_PARSER, 'GenericCrawler'),
    )

    LOCAL = '0'
    S3 = '1'
    STORAGE_CHOICE = (
        (LOCAL, 'local'),
        (S3, 's3'),
    )

    TEXT = '0'
    IMAGES = '1'
    TEXT_AND_IMAGES = '2'
    TYPE_CHOICE = (
        (TEXT, 'text'),
        (IMAGES, 'images'),
        (TEXT_AND_IMAGES, 'text and images')
    )

    depth = models.IntegerField(null=False, blank=False, default=1)

    parser = models.CharField(max_length=1, null=False, blank=False, default=0, choices=PARSER_CHOICE)
    crawler = models.CharField(max_length=1, null=False, blank=False, default=0, choices=CRAWLER_CHOICE)
    task_type = models.CharField(max_length=1, null=False, blank=False, default=2, choices=TYPE_CHOICE)

    target_url = models.URLField(max_length=255, null=False, blank=False)

    images_storage = models.CharField(max_length=1, null=False, blank=False, default=0, choices=STORAGE_CHOICE)
    images_max_size = models.IntegerField(default=settings.DEFAULT_MAX_SIZE)

    done = models.BooleanField(default=False)

    @property
    def parse_images(self):
        if self.task_type in (self.IMAGES, self.TEXT_AND_IMAGES):
            return True
        return False

    @property
    def parse_text(self):
        if self.task_type in (self.TEXT, self.TEXT_AND_IMAGES):
            return True
        return False
