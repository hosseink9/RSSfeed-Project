import pika
import uuid
import json

class Publish:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.chanel = self.connection.channel()
        result = self.chanel.queue_declare(queue = '', exclusive = True)
        self.qname = result.method.queue

