import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trade_app.settings')

app = Celery('trade_app')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-offers-every-minute': {
        'task': 'trades.tasks.offers_handler',
        'schedule': 60.0,
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
