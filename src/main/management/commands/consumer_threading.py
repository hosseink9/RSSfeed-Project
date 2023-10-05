from typing import Any
from django.core.management import BaseCommand
from main.publisher import Publish

from consumer import login_consume, register_consume, update_podcast_consume

import threading


