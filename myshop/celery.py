import os
import time
from symbol import test

from celery import Celery
from celery.schedules import crontab

from myshop import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery("myshop")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
#     time.sleep(5)
#     print('Hi Oleg')
#
# @app.task
# def add(x, y):
#     return x + y

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 10.0,
        'args': {4, 4}
    },
}
app.conf.timezone = 'UTC'
