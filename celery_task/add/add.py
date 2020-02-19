from celery_task.main import app


@app.task
def add(x, y):
    return x + y