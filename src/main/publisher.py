import pika
import uuid
import json

from config import settings

class Publish:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
        self.chanel = self.connection.channel()
        result = self.chanel.queue_declare(queue = '', exclusive = True)
        self.qname = result.method.queue

    def login(self, username, request_META):
        notification={
            'username' : username,
            'message' : f"{username} is login",
            'user_agent': request_META,
            'routing_key': 'login'
        }
        self.response = None
        # self.corr_id = str(uuid.uuid4())
        self.chanel.basic_publish(exchange = '', routing_key = 'login',
                                    properties = pika.BasicProperties(delivery_mode=2), body = json.dumps(notification)) # properties = pika.BasicProperties(reply_to = self.qname, correlation_id=self.corr_id)

    def register(self, username, request_META):
        notification={
            'username' : username,
            'message' : f"{username} is register",
            'user_agent': request_META,
            'routing_key': 'register'
        }
        self.response = None
        # self.corr_id = str(uuid.uuid4())
        self.chanel.basic_publish(exchange = '', routing_key = 'register',properties = pika.BasicProperties(delivery_mode=2), body = json.dumps(notification))

    def update_podcast(self, podcast):
        notification={
            'podcast' : podcast.id,
            'message' : f"{podcast.title} has new episodes",
            'routing_key': 'update_podcast'
        }
        self.response = None
        self.chanel.basic_publish(exchange = '', routing_key = 'update_podcast',
                                    properties = pika.BasicProperties(delivery_mode=2), body = json.dumps(notification))

