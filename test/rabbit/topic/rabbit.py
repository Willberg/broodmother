import pika

__conn = None


def rabbit_connect(host, port, username, password, vhost):
    credentials = pika.PlainCredentials(username, password)
    param = pika.ConnectionParameters(host, port, vhost, credentials, heartbeat=10)
    global __conn
    __conn = pika.BlockingConnection(param)


def rabbit_disconnect():
    if __conn is not None:
        __conn.close()


def rtz_put(message):
    if not __conn:
        print("rabbit mq connection disconnect")
        return

    # 获取channel
    channel = __conn.channel()

    # 采用topic exchange
    channel.exchange_declare(exchange='rtz', exchange_type='topic')

    channel.basic_publish(
        exchange='rtz',
        routing_key='rtz.images',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )


def rabbit_message_process(exchange, exchange_type, queue_name, routing_key, process_message):
    if not __conn:
        print("rabbit mq connection disconnect")
        return

    # 获取channel
    channel = __conn.channel()

    # 采用topic exchange
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)

    channel.queue_declare(queue_name, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)

    # 防止worker负载过多，导致其他worker负载过少
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=process_message
    )

    channel.start_consuming()
