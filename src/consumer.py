import pika
import json
import time
import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from users.models import User, Notification, NotificationInfo
from feedback.models import Playlist



def login_callback(chanel, method, properties, body):
    data = json.loads(body)
    user = User.objects.get(username=data['username'])
    notification_info = NotificationInfo.objects.create(message=data['message'])
    Notification.objects.create(user = user, message = notification_info)

def login_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    chanel = connection.channel()

    chanel.queue_declare(queue='login')
    chanel.basic_consume(queue='login', on_message_callback=login_callback)

    chanel.start_consuming()


def register_callback(chanel, method, properties, body):
    data = json.loads(body)
    user = User.objects.get(username=data['username'])
    notification_info = NotificationInfo.objects.create(message=data['message'])
    Notification.objects.create(user = user, message = notification_info)

def register_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    chanel = connection.channel()

    chanel.queue_declare(queue='register')
    chanel.basic_consume(queue='register', on_message_callback=login_callback)

    chanel.start_consuming()


def update_podcast_callback(chanel, method, properties, body):
    data = body

    playlist = Playlist.objects.get(podcasts = data['podcast'])

    for detail in playlist:
        notification = NotificationInfo.objects.create(message = data['message'])
        user = User.objects.get(id = detail.user.id)
        Notification.objects.create(user = user, message = notification)

