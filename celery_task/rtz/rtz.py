import json

import requests
from celery import Celery

# amqp://myuser:mypassword@localhost:5672/myvhost
from celery_task.utils.rabbit import rabbit_connect, rabbit_message_process

app = Celery('rtz', broker='amqp://root:123456@192.168.0.105:5672/rtz')


def process_message(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

    # 请求rtz接口
    headers = {
        'service': 'rtz_0001',
        'secret': 'bd3273c7a37b5ab33ed3e996d14f744d'
    }
    req_data = json.loads(body)
    res = requests.put('http://127.0.0.1:10002/api/fs/v1/rtz/save', headers=headers, data=req_data)

    # 发送确认,删除消息
    ch.basic_ack(delivery_tag=method.delivery_tag)


@app.task
def insert_to_db():
    # 从rabbit取数据
    rabbit_connect('192.168.0.105', 5672, 'root', '123456', 'rtz')
    rabbit_message_process('rtz', 'topic', 'rtz', 'rtz.images', process_message)
