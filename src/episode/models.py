from django.db import models

from podcast.models import Podcast
from main.models import BaseModel
from author.models import Author

class Episode(BaseModel):
    title = models.CharField(max_length=100) #We use title for itunes title and handel it in view
    guid = models.CharField(max_length=50)
    itunes_duration = models.CharField(max_length=50)
    itunes_episodeType = models.CharField(max_length=50)
    itunes_explicit = models.CharField(max_length=50)

    #We use description for itunes summary and content_encoded and handel this in view
    description = models.TextField(null=True,blank=True)
    link = models.URLField(null=True,blank=True)
    pubDate = models.DateTimeField(null=True,blank=True)
    itunes_keywords = models.TextField(null=True, blank=True)

    podcast = models.ForeignKey(Podcast,on_delete=models.CASCADE)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)


    def __str__(self):
        return self.title