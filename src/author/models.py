from django.db import models


class PodcastAuthor(models.Model):
    name = models.CharField(max_length=30)

