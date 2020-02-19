import json

import requests


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
    # ch.basic_ack(delivery_tag=method.delivery_tag)