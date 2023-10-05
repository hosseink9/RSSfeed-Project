from typing import Any
from django.core.management import BaseCommand
from main.publisher import Publish

from consumer import login_consume, register_consume, update_podcast_consume

import threading


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):

        login_thread =threading.Thread(target=login_consume)
        register_thread =threading.Thread(target=register_consume)
        update_podcast_thread =threading.Thread(target=update_podcast_consume)

        login_thread.start()
        register_thread.start()
        update_podcast_thread.start()