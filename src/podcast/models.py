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


class Generator(BaseModel):
    name = models.CharField(max_length=100)

    hostname = models.CharField(max_length=150,null=True,blank=True)
    genDate = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.name


class Podcast(BaseModel):
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    itunes_type = models.CharField(max_length=50)
    copy_right = models.CharField(max_length=100)
    explicit = models.CharField(max_length=50)
    #We use description for itunes summary and handel this in view
    description = models.TextField()

    pubDate = models.DateTimeField(null=True,blank=True)
    last_build_date = models.DateTimeField(null=True,blank=True)
    link = models.URLField(null=True,blank=True)
    itunes_subtitle = models.TextField(null=True,blank=True)
    itunes_keywords = models.TextField(null=True, blank=True)

    category = models.ManyToManyField(Category)
    generator = models.ForeignKey(Generator,on_delete=models.CASCADE)
    podcast_author = models.ForeignKey(PodcastAuthor,on_delete=models.SET_NULL)
    image = models.OneToOneField(Image,on_delete=models.SET_NULL)

    def __str__(self):
        return self.title