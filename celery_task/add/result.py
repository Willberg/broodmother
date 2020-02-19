import time

from celery.result import AsyncResult

from celery_task.add.add import add
from celery_task.celery_tasks import app

result = add.delay(4, 5)
print(result.id)
async_result = AsyncResult(id=result.id, app=app)

status = async_result.successful()
while not status:
    time.sleep(1)
    status = async_result.successful()

print(async_result.get())

# if async_result.successful():
#     result = async_result.get()
#     print(result)
#     # result.forget() # 将结果删除
# elif async_result.failed():
#     print('执行失败')
# elif async_result.status == 'PENDING':
#     print('任务等待中被执行')
# elif async_result.status == 'RETRY':
#     print('任务异常后正在重试')
# elif async_result.status == 'STARTED':
#     print('任务已经开始被执行')
