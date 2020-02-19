import time

from celery.result import AsyncResult

from celery_task.celery_tasks import app
from celery_task.rtz_test.rtz_test import insert_to_db

result = insert_to_db.delay()
print(result.id)
async_result = AsyncResult(id=result.id, app=app)

status = async_result.successful()
while not status:
    time.sleep(1)
    status = async_result.successful()

print(async_result.get())
