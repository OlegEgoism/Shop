import time

from celery import shared_task

from celery import Celery

app = Celery('tasks', backend='redis://localhost:6379', broker='redis://127.0.0.1:6379/0')



# @shared_task(track_started=True)
@app.task(track_started=True)
def add(x):
    time.sleep(5)
    return x*x
