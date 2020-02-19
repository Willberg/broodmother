from celery import Celery

app = Celery(
    'main',
    broker='amqp://root:123456@192.168.0.105:5672/rtz',
    backend='redis://root:test123@192.168.0.105:6379/4',
    # 包含以下两个任务文件，去相应的py文件中找任务，对多个任务做分类
    include=[
        'celery_task.rtz_test.rtz_test',
        # 'celery_task.add.add',
    ]
)

# 时区
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False

if __name__ == '__main__':
    app.worker_main()
