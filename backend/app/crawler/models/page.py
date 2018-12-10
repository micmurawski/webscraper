from django.db import models

from app.crawler.search import PageIndex
from app.media.models import Image

from .core import TimestampedModel
from .task import Task


class Page(TimestampedModel):
    task = models.ForeignKey(Task, related_name='pages', on_delete=models.CASCADE)
    target_url = models.URLField(max_length=255, null=False, blank=False)
    error = models.BooleanField(default=False)

    text = models.TextField()
    images = models.ManyToManyField(Image, blank=True)

    done = models.BooleanField(default=False)

    class Meta:
        unique_together = ('task', 'target_url',)

    def indexing(self):
        obj = PageIndex(
            meta={'id': self.id},
            text=self.text
        )
        obj.save()
        return obj.to_dict(include_meta=True)
