from celery import shared_task
import requests
from podcast.utils import Parser
from podcast.tasks import RetryTask
from podcast.models import Podcast


@shared_task
def update_all_podcast():
    url_list = Podcast.objects.all().values_list('podcast_url')
    for url in url_list:
        update_podcast.delay(url)


@shared_task(bind=True, base=RetryTask)
def update_podcast(self,url):
    data = requests.get(url).text
    parser = Parser(data)
    parser.update_exist_podcast()

    if self.request.retries > self.retry_kwargs['max_retries']:
        logger.error(f'{self.request.retries},{self.retry_kwargs["max_retries"]}')
    elif self.request.retries == self.retry_kwargs['max_retries']:
        logger.error("Task isn't successfully")