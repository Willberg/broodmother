from celery.result import AsyncResult

from celery_task.main import app

async_result = AsyncResult(id="1affdc20-b625-4cf3-a6a4-11b3b6fdf6f4", app=app)

if async_result.successful():
    result = async_result.get()
    print(result)
    # result.forget() # 将结果删除
elif async_result.failed():
    print('执行失败')
elif async_result.status == 'PENDING':
    print('任务等待中被执行')
elif async_result.status == 'RETRY':
    print('任务异常后正在重试')
elif async_result.status == 'STARTED':
    print('任务已经开始被执行')
