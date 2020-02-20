import time

from celery.result import AsyncResult

from celery_task.celery_tasks import app
from celery_task.rtz.rtz import send_to_db

result = send_to_db.delay()
print(result.id)
async_result = AsyncResult(id=result.id, app=app)

retry = 0
status = async_result.successful()
while not status:
    status = async_result.successful()
    time.sleep(1)
    print('retry times %d' % retry)
    retry += 1

print(async_result.get())
