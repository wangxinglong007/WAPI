# !/usr/bin/env python
# coding:utf-8

import pika
import redis
from Rsa_encrypt.js import rsa_encryption_data

credentials = pika.PlainCredentials('admin', 'admin')
parameters = pika.ConnectionParameters('xxxx', 'port', 'xxxxTest', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='AutoPayQueue')
print '[*] Waiting for messages. To exit press CTRL+C'
r = redis.Redis(host='xxx', port=port)


def callback(ch, method, properties, body):

    list_body = eval(body).items()[0]
    # print list_body[0], rsa_encryption_data(list_body[1])
    r.set(list_body[0], rsa_encryption_data(list_body[1]), ex=1800)
# channel.basic_consume(callback, queue = 'queue.abs.booking.searchflightlist' , no_ack = True )
channel.basic_consume(callback, queue='AutoPayQueue', no_ack=True)
channel.start_consuming()

