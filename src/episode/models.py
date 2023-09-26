from django.db import models

from podcast.models import Podcast
from main.models import BaseModel
from author.models import EpisodeAuthor

class Episode(models.Model):
    title = models.CharField(max_length=100) #We use title for itunes_title too.
    guid = models.CharField(max_length=50)
    itunes_duration = models.CharField(max_length=50)
    itunes_episode_type = models.CharField(max_length=50)
    itunes_explicit = models.CharField(max_length=50)
    description = models.TextField() #We use description for itunes summary and content_encoded too.
    enclosure = models.CharField(null=True, blank=True,max_length=100)
    link = models.URLField(null=True,blank=True)
    pubDate = models.DateTimeField(null=True,blank=True)
    itunes_keywords = models.TextField(null=True, blank=True)
    itunes_player = models.CharField(null=True, blank=True,max_length=100) #We use itunes_player for fireside_playerEmbedCode too.
    episode_podcast = models.ForeignKey(Podcast,on_delete=models.CASCADE, related_name="episode")
    episode_author = models.ForeignKey(EpisodeAuthor,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.title}"