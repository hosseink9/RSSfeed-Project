from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from main.models import BaseModel
from users.models import User
from podcast.models import Podcast
