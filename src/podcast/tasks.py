from celery import shared_task, Task
import logging
import requests

from .utils import Parser
from .models import Podcast, PodcastUrl

logger = logging.getLogger('django-celery')


class RetryTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2



@shared_task(bind=True, base=RetryTask)
def save_podcast(self,url):

    logger.info(msg='Podcast going to parsing')
    data = requests.get(url).text
    podcast_url = PodcastUrl.objects.get(url=url)
    Parser(podcast_url=podcast_url, rss_file=data, save=True)

    if self.request.retries > self.retry_kwargs['max_retries']:
        logger.error(f'{self.request.retries},{self.retry_kwargs["max_retries"]}')
    elif self.request.retries == self.retry_kwargs['max_retries']:
        logger.error("Task isn't successfully")
    return 'Podcast going to parsing'
