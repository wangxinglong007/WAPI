import pika
import time
import uuid
import json
import redis
# channel.queue_declare(queue='queue.abs.booking.searchflightlist')


def send_to_rmq(org_data):
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters('host', 'port', 'xxxxTest', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    uuid_ = uuid.uuid4().__str__()
    body = str({uuid_: org_data})
    channel.basic_publish(exchange='',
                          # routing_key='queue.abs.booking.searchflightlist',
                          routing_key='AutoPayQueue',
                          body=body)
    # print " [x] Sent %s" %body
    connection.close()
    return uuid_


def uuid_get_data(uuid):
    r = redis.Redis(host='host', port='port')
    while r.get(uuid) is None:
        time.sleep(0.5)
    return r.get(uuid)


def rsa_data(need_data):
    return eval(uuid_get_data(send_to_rmq(need_data)))


