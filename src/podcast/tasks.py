from celery import shared_task, Task
import requests

from .utils import Parser
from .models import PodcastUrl
from .task_log import log_task_info


class RetryTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2
    retry_jitter = False
    task_acks_late = True
    worker_concurrency = 4
    prefetch_multiplier = 1


    def on_failure(self, exc, task_id, args, kwargs, einfo):
        log_task_info(self.name, 'error', f'Task {self.name} failed: {str(exc)}',task_id, args, kwargs, exception=exc)




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
