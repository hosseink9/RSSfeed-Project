from .utils import log_format
import json
import logging

logger = logging.getLogger('elastic-logger')


def log_to_elasticsearch(log_data, log_level):
    if log_level == 'info':
        logger.info(json.dumps(log_data))
    elif log_level == 'error':
        logger.error(json.dumps(log_data))


