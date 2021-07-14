from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab  # scheduler

# default django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlakeFinder.settings')

app = Celery('FlakeFinder',
             broker='amqp://',
             backend='rpc://',
             include=['scraping.tasks'])
app.conf.timezone = 'UTC'
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # executes every three hours
    'scraping-task-three-hr': {
        'task': 'scraping.tasks',
        'schedule': crontab()
    }
}

if __name__ == '__main__':
    app.start()
