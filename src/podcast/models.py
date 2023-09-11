from django.db import models

from main.models import BaseModel
from author.models import PodcastAuthor


class Category(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Owner(BaseModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Image(BaseModel):
    url = models.URLField()

    title = models.CharField(max_length=100,null=True,blank=True)
    link = models.URLField(null=True,blank=True)

class Podcast(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    pubDate = models.DateTimeField()
    link = models.URLField(null=True,blank=True)
    language = models.CharField(max_length=50)
    itunes_subtitle = models.TextField(null=True,blank=True)
    itunes_type = models.CharField(max_length=50)
    category = models.ManyToManyField(Category)
    podcast_author = models.ForeignKey(PodcastAuthor,on_delete=models.SET_NULL)
    image = models.OneToOneField(Image,on_delete=models.SET_NULL)

    def __str__(self):
        return self.title