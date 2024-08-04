

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
import environ

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventoryPlus.settings')

# Initialise environment variables
env = environ.Env()
environ.Env.read_env() 

app = Celery('InventoryPlus')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-low-stock-alerts-every-day': {
        'task': 'inventory.tasks.send_low_stock_alerts_task',
        'schedule': crontab(minute=0, hour=0),  # Every day at midnight
    },
    'send-expiry-alerts-every-day': {
        'task': 'inventory.tasks.send_expiry_alerts_task',
        'schedule': crontab(minute=0, hour=1),  # Every day at 1 AM
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


