from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.state import User

from trades.models import Inventory


@receiver(post_save, sender=User)
def create_empty_inventory(sender, instance, *args, **kwargs):
    Inventory(user=instance).save()
