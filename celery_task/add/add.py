from celery_task.celery_tasks import app


@app.task
def add(x, y):
    return x + y