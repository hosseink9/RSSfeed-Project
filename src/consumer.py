import pika
import json
import time
import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from users.models import User, Notification, NotificationInfo
from feedback.models import Playlist
