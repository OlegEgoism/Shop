# import time
#
# from celery import shared_task
#
# from celery import Celery
#
# app = Celery('tasks', backend='redis://localhost:6379', broker='redis://127.0.0.1:6379/0')
#
#
#
# # @shared_task(track_started=True)
# @app.task(track_started=True)
# def add(x):
#     time.sleep(5)
#     return x*x

from celery import Celery
from celery.schedules import crontab

# app = Celery()
app = Celery('tasks', backend='redis://localhost:6379', broker='redis://127.0.0.1:6379/0')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

@app.task
def test(arg):
    print(arg)

# @app.task
# def add(x, y):
#     z = x + y
#     print(z)


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.test',
        'schedule': 10.0,
        'args': {'id': 2}
    },
}
app.conf.timezone = 'UTC'