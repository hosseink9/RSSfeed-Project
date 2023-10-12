from .utils import log_format
import json
import logging

logger = logging.getLogger('elastic-logger')


def log_to_elasticsearch(log_data, log_level):
    if log_level == 'info':
        logger.info(json.dumps(log_data))
    elif log_level == 'error':
        logger.error(json.dumps(log_data))


class LoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        log_data = log_format(request, response)
        log_to_elasticsearch(log_data, log_level='info')
        return response

    def process_exception(self, request, exception):
        log_data = log_format(request, None, exception)
        log_to_elasticsearch(log_data, log_level='error')