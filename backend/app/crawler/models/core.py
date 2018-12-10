from django.db import models
from django.utils.timezone import now


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.updated_at = now()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta:
        abstract = True
