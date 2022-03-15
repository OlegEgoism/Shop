import os
import time
from celery import Celery
from myshop import settings

app = Celery('orders')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redis_celery.settings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(track_started=True)
def add(x):
    time.sleep(20)
    return x**x
