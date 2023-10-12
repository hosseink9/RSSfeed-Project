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

    def retry(self, args=None, kwargs=None, exc=None, throw=True,
              eta=None, countdown=None, max_retries=None, **options):
        retry_count = self.request.retries
        retry_eta = eta or (countdown and f'countdown={countdown}') or 'default'
        log_task_info(self.name, 'warning', f'Retrying task {self.name} (retry {retry_count}) in {retry_eta} seconds',self.request.id, args, kwargs, exception=exc, retry_count=retry_count, max_retries=max_retries, retry_eta=retry_eta)

        super().retry(args, kwargs, exc, throw, eta, countdown, max_retries, **options)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        log_task_info(self.name, 'error', f'Task {self.name} failed: {str(exc)}',task_id, args, kwargs, exception=exc)

    def on_success(self, retval, task_id, args, kwargs):
        log_task_info(self.name, 'info', f'Task {self.name} completed successfully', task_id, args, kwargs, retval)



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
