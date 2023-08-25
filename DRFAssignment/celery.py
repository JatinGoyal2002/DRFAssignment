# from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRFAssignment.settings')

app = Celery('DRFAssignment')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'send_daily_mail',
        'schedule': crontab(hour=0, minute=0),
        # 'schedule': 30.0,
        # 'args': ('')
    },
}
app.conf.timezone = 'ASIA/KOLKATA'
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))