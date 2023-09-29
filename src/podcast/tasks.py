from celery import shared_task, Task
from django.db.models import Max
import datetime as dt
from time import sleep
import logging

from .models import Podcast
from episode.models import Episode
from author.models import PodcastAuthor, EpisodeAuthor

logger = logging.getLogger('django-celery')


class RetryTask(Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2




