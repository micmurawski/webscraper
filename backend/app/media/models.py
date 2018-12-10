from django.db import models


class Image(models.Model):
    S3 = '1'
    LOCAL = '0'
    BACKENDS = ((LOCAL, 'local'), (S3, 's3'),)

    storage = models.CharField(max_length=255, choices=BACKENDS, default=LOCAL)
    url = models.URLField(max_length=255, null=False, blank=False)
    filename = models.CharField(max_length=255, null=False, blank=False)
    path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.url
