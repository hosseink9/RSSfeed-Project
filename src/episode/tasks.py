from celery import shared_task
import requests
from podcast.utils import Parser
from .models import Episode
from podcast.models import Podcast
import logging

logger = logging.getLogger('django-celery')

