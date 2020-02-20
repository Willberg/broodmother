import json

from test.rabbit.topic.rabbit import rabbit_connect, rtz_put, rabbit_disconnect

rabbit_connect('192.168.0.105', 5672, 'root', '123456', 'rtz')
# 发送rabbit消息
data = {
    'doc_id': '123',
    'title': 'title',
    'family': 'family',
    'tags': 'tags'

}
print(data)
rtz_put(json.dumps(data))

# rabbit_disconnect()
