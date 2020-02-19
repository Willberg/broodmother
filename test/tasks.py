from celery import Celery

app = Celery('tasks', broker='amqp://root:123456@192.168.0.105:5672/rtz',
             backend='redis://root:test123@192.168.0.105:6379/4')


@app.task
def add(x, y):
    return x + y
