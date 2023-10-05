import pika
import uuid
import json

class Publish:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.chanel = self.connection.channel()
        result = self.chanel.queue_declare(queue = '', exclusive = True)
        self.qname = result.method.queue

    def login(self, username, request_META):
        notification={
            'username' : username,
            'message' : f"{username} is login; {request_META}"
        }
        self.response = None
        # self.corr_id = str(uuid.uuid4())
        self.chanel.basic_publish(exchange = '', routing_key = 'login',
                                    properties = pika.BasicProperties(delivery_mode=2), body =json.dumps(notification)) # properties = pika.BasicProperties(reply_to = self.qname, correlation_id=self.corr_id)

