import time

from celery import shared_task

from celery import Celery

app = Celery('tasks', broker='redis://127.0.0.1:6379/0')



@app.task
def add(x):
    # time.sleep(15)
    return x*x
