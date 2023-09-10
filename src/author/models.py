from django.db import models


class PodcastAuthor(models.Model):
    name = models.CharField(max_length=30)


class EpisodeAuthor(models.Model):
    name = models.CharField(max_length=30)