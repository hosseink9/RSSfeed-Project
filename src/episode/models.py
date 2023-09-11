from django.db import models

from podcast.models import Podcast
from main.models import BaseModel
from author.models import EpisodeAuthor,PodcastAuthor

class Episode(BaseModel):
    title = models.CharField(max_length=100)
    guid = models.CharField(max_length=50)

    description = models.TextField(null=True,blank=True) #We use description for itunes summary and handel this in view
    link = models.URLField(null=True,blank=True)
    pubDate = models.DateTimeField(null=True,blank=True)
    itunes_keywords = models.TextField(null=True, blank=True)

    podcast = models.ForeignKey(Podcast,on_delete=models.CASCADE)
    episode_author = models.ForeignKey(EpisodeAuthor,on_delete=models.SET_NULL)


    def __str__(self):
        return self.title