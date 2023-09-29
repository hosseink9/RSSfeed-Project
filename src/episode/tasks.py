from celery import shared_task
import requests
from podcast.utils import Parser
from .models import Episode
from podcast.models import Podcast
import logging

logger = logging.getLogger('django-celery')


@shared_task
def update_all_podcast():
    url_list = Podcast.objects.all().values_list('url')
    for url in url_list:
        update_podcast.delay(url)

