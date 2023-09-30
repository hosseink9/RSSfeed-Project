from celery import shared_task, Task
import logging

from .utils import Parser


logger = logging.getLogger('django-celery')


class RetryTask(Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2



@shared_task(bind=True, base=RetryTask)
def save_episode(self,file):
    Parser(rss_file=file.decode("utf-8"), save=True)
    return 'OK'


@shared_task(bind=True, base=RetryTask,)
def update_task(self,file):
    parser = Parser(rss_file=file.decode("utf-8"))
    parser.update_exist_podcast()
    if self.request.retries > self.retry_kwargs['max_retries']:
        logger.error(f'{self.request.retries},{self.retry_kwargs["max_retries"]}')
    elif self.request.retries == self.retry_kwargs['max_retries']:
        logger.error("[Task isn't successfully]")

    return 'OK'



