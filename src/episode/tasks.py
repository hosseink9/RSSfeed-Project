from celery import shared_task
import requests
from podcast.utils import Parser
from podcast.tasks import RetryTask
from podcast.models import Podcast


@shared_task
def update_all_podcast():
    podcast = Podcast.objects.all()
    for podcast_urls in podcast:
        update_podcast.delay(url=str(podcast_urls.podcast_url.url))
    return "Url sent to parsing!"


@shared_task(bind=True, base=RetryTask)
def update_podcast(self,url):
    data = requests.get(url).text
    parser = Parser(data)
    parser.update_exist_podcast()

    if self.request.retries > self.retry_kwargs['max_retries']:
        logger.error(f'{self.request.retries},{self.retry_kwargs["max_retries"]}')
    elif self.request.retries == self.retry_kwargs['max_retries']:
        logger.error("Task isn't successfully")