from celery import Celery
from celery.schedules import crontab

# 创建celery实例，并注册任务
cel = Celery(
    'tasks',
    broker='amqp://root:123456@192.168.0.105:5672/rtz',
    backend='redis://root:test123@192.168.0.105:6379/4',
    include=[
        'celery_contab.add.add',
    ]
)

cel.conf.timezone = 'Asia/Shanghai'
cel.conf.enable_utc = False

# 配置定时任务和该执行的任务
cel.conf.beat_schedule = {
    'update_rtz_index_every_day': {
        'task': 'celery_contab.add.add.add',
        'schedule': crontab(minute='*/1'),
        'args': (1, 2)
    }
}

# celery -A celery_contab beat 发布任务
# celery -A celery_contab worker --loglevel=info 执行任务
# 都在项目根目录下执行
