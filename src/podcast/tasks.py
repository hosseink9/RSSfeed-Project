from celery import shared_task, Task
import logging

from .utils import Parser


logger = logging.getLogger('django-celery')


class RetryTask(Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2



@shared_task(bind=True, base=RetryTask)
def save_podcast(self,url):
    try:
        logger.info(msg='Podcast going to parsing')
        data = requests.get(url).text
        podcast_url = PodcastUrl.objects.get(url=url)
        Parser(podcast_url=podcast_url, rss_file=data, save=True)

        if self.request.retries > self.retry_kwargs['max_retries']:
            logger.error(f'{self.request.retries},{self.retry_kwargs["max_retries"]}')
        elif self.request.retries == self.retry_kwargs['max_retries']:
            logger.error("[Task isn't successfully]")

    except ConnectionError as e:
        logger.error(e)
    return 'OK'
