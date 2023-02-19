import os

from celery import Celery
from celery.schedules import crontab
from .settings import TIME_ZONE

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flatdata.settings')

app = Celery('flatdata')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.timezone = TIME_ZONE
app.conf.beat_schedule = {
    'update_coefficient': {
        'task': 'data.tasks.update_coefficients',
        'schedule': crontab(minute=55, hour=3)
    }
}
