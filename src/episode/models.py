from django.db import models

from podcast.models import Podcast
from main.models import BaseModel
from author.models import EpisodeAuthor

class Episode(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    pubDate = models.DateTimeField()
    link = models.URLField(null=True,blank=True)
    guid = models.CharField(max_length=50)
    itunes_summery = models.TextField()
    podcast = models.ForeignKey(Podcast,on_delete=models.CASCADE)
    episode_author = models.ForeignKey(EpisodeAuthor,on_delete=models.SET_NULL)


    def __str__(self):
        return self.title