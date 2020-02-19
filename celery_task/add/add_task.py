from celery_task.add.add import add

result = add.delay(4, 5)
print(result.id)
