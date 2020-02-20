#!/usr/bin/env python
# -*- coding:utf-8 -*-

# credentials = pika.PlainCredentials('ethan', 'ethan123456')  # 用户名密码
#
# # 四个参数分别是  BrokerIP  BrokerPort, Vhost, username_and_password, 心跳时间间隔
# parameter = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials, heartbeat_interval=0)
#
# connection = pika.BlockingConnection(parameter)  # 建立连接
# channel = connection.channel()        # 获得连接的channel对象
#
# channel.queue_declare(queue="yanchampion")   # queue声明
#
# channel.basic_publish(
#     exchange='',
#     routing_key='yanchampion',
#     body='Hello pika!'
# )                                        # basic_publish方法发送消息
#
# print("[X] send 'Hello pika!'")
# connection.close()                       # 关闭连接


from test.rabbit.sample.rabbit import RabbitMQ

# RabbitMQ类的初始化参数，包括broker_ip, port, username, password, vhost
args = ("192.168.0.105", 5672, "root", "123456", "rtz")
mq = RabbitMQ(*args)  # 传入初始化参数
mq.connect()  # 调用connect方法，连接broker

# 调用put方法，向目标queue中发送数据， 第一个参数是data, 第二个参数是queue_name, 第三个参数是route_name
mq.put("hello RabbitMQ!!!", "yanchampion", "yanchampion")

# 发完数据，主动关闭连接
mq.close()
