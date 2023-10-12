import json
import logging
import time
from datetime import datetime
from config import settings
from elasticsearch import Elasticsearch
import pytz
from config import settings

tz = pytz.timezone(settings.TIME_ZONE)

class ElasticHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.es = Elasticsearch(f'http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}')
        self.sender = LogSender(self.es)

    def emit(self, record):
        try:
            self.sender.writeLog(record, formatter=self.format)
        except Exception:
            self.handleError(record)


