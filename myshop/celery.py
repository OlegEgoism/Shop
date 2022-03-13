import os
import time

from celery import Celery

from myshop import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery("myshop")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
#     time.sleep(5)
#     print('Hi Oleg')

# @app.task
# def add(x, y):
#     return x + y


