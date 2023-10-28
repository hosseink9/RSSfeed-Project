import pika
import json
import time
import os
import logging

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from users.models import User, Notification, NotificationInfo
from feedback.models import Playlist
from config import settings
from podcast.models import Podcast
from main.utils import authentication_log_format, rss_log_format

logger = logging.getLogger('elastic-logger')


def login_callback(chanel, method, properties, body):
    data = json.loads(body)
    user = User.objects.get(username=data['username'])
    notification_info = NotificationInfo.objects.create(message=data['message'])
    Notification.objects.create(user = user, message = notification_info)

def login_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
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
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    chanel = connection.channel()

    chanel.queue_declare(queue='register')
    chanel.basic_consume(queue='register', on_message_callback=login_callback)

    chanel.start_consuming()


def update_podcast_callback(chanel, method, properties, body):
    data = json.loads(body)

    playlists = Podcast.objects.get(id=data['podcast']).playlist_set.all()
    for playlist in playlists:
                notification = NotificationInfo.objects.create(message = data['message'])
                user = User.objects.get(id=playlist.account.id)
                Notification.objects.create(user = user, message = notification)

def update_podcast_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    chanel = connection.channel()

    chanel.queue_declare(queue='update_podcast')

    chanel.basic_consume(queue='update_podcast', on_message_callback=update_podcast_callback)

    chanel.start_consuming()
