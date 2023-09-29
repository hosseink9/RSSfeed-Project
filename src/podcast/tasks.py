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



@shared_task(bind=True, base=RetryTask)
def author(self,episode_list):
    author_list = list()
    dict_list = dict()

    for episode in episode_list:
        author = dict_list.get(episode.get("itunes_author")) or EpisodeAuthor.objects.get_or_create(name=episode.get("itunes_author"))[0] if episode.get('itunes_author') else None
        dict_list[episode.get("itunes_author")] = author
        author_list.append(author)

    author_list = list(map(lambda author:author.id if author else None,author_list))
    return author_list




