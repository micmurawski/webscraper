from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.page import Page


@receiver(post_save, sender=Page)
def index_page(sender, instance, **kwargs):
    if not settings.UNIT_TESTING:
        instance.indexing()
