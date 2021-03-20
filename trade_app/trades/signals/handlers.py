from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.state import User

from trades.models import (
    WatchList,
    Inventory,
)


@receiver(post_save, sender=User)
def create_empty_inventory_and_watchlist(sender, instance, *args, **kwargs):
    WatchList(user=instance).save()
    Inventory(user=instance).save()
