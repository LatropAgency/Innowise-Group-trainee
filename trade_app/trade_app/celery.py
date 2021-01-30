from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trade_app.settings')

app = Celery('trade_app')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@shared_task
def task(name):
    return f'Hello {name}'
