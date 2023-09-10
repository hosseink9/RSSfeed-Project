from django.db import models


class PodcastAuthor(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class EpisodeAuthor(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name