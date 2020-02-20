#!/usr/bin/env python
# -*- coding:utf-8 -*-

#
# credentials = pika.PlainCredentials('ethan', 'ethan123456')
# parameter = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials, heartbeat_interval=10)
# connection = pika.BlockingConnection(parameter)
#
# channel = connection.channel()
#
# channel.queue_declare(queue="yanchampion")
#
#
# def callback(ch, method, properties, body):
#     print "[x] Received {0}".format(body)
#
#
# channel.basic_consume(callback,
#                       queue='yan',
#                       no_ack=True)
#
# print "[*] waiting for messages. To exit press CTR+CL"
# channel.start_consuming()

from test.rabbit.sample.rabbit import RabbitMQ

# RabbitMQ类的初始化参数，包括broker_ip, port, username, password, vhost
args = ("192.168.0.105", 5672, "root", "123456", "rtz")
mq = RabbitMQ(*args)  # 传入初始化参数
mq.connect()  # 调用connect方法，连接broker

mq.getting_start("yanchampion")  # 调用getting_start方法从queue中获取data， 传入的参数是queue_name
