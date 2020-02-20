from test.rabbit.topic.rabbit import rabbit_message_process, rabbit_connect

rabbit_connect('192.168.0.105', 5672, 'root', '123456', 'rtz')


def process_message(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

    # 发送确认,删除消息
    print(method.delivery_tag)
    ch.basic_ack(delivery_tag=method.delivery_tag)


rabbit_message_process('rtz', 'topic', 'rtz', 'rtz.images', process_message)
