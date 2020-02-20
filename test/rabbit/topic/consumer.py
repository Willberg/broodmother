import json

import requests

from test.rabbit.topic.rabbit import rabbit_message_process, rabbit_connect

rabbit_connect('192.168.0.105', 5672, 'root', '123456', 'rtz')


def process_message(ch, method, properties, body):
    # print(" [x] %r:%r" % (method.routing_key, body))
    print('result: %s' % json.loads(body))

    # 发送确认,删除消息
    print(method.delivery_tag)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def save(ch, method, properties, body):
    # 请求rtz接口
    headers = {
        'service': 'rtz_0001',
        'secret': 'bd3273c7a37b5ab33ed3e996d14f744d'
    }
    req_data = json.loads(body)
    res = requests.put('http://127.0.0.1:10002/api/fs/v1/rtz/save', headers=headers, data=req_data).content
    if not res:
        print('error %s' % str(body))
        return None

    res_json = json.loads(res)
    if not res_json['status']:
        print('error %s' % str(body))
        return None

    print(res_json['data'])

    # 发送确认,删除消息
    ch.basic_ack(delivery_tag=method.delivery_tag)


rabbit_message_process('rtz', 'topic', 'rtz', 'rtz.images', save)
