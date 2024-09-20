from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import NoprizFiz


@receiver(post_save, sender=NoprizFiz)
@receiver(post_delete, sender=NoprizFiz)
def clear_NoprizFiz_cache(sender, instance, **kwargs):
    keys = cache.keys("views.decorators.cache.cache*")
    cache.delete_many(keys)
