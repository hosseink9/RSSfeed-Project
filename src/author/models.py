from django.db import models

from main.models import BaseModel

class PodcastAuthor(BaseModel):
    name = models.CharField(max_length=30)


    def __str__(self):
        return self.name


class EpisodeAuthor(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)


    def __str__(self):
        return self.name