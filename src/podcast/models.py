from django.db import models

from main.models import BaseModel
from author.models import PodcastAuthor


class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Owner(BaseModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Image(BaseModel):
    url = models.CharField(max_length=150,null=True,blank=True)

    title = models.CharField(max_length=100,null=True,blank=True)
    link = models.URLField(null=True,blank=True)

    def __str__(self):
        return f'{self.url}'


class Generator(BaseModel):
    name = models.CharField(max_length=100)

    hostname = models.CharField(max_length=150,null=True,blank=True)
    genDate = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.name


class Podcast(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(null=True,blank=True)
    language = models.CharField(max_length=50)
    itunes_type = models.CharField(max_length=50)
    copy_right = models.CharField(max_length=100)
    explicit = models.CharField(max_length=50)
    description = models.TextField() #We use description for itunes summary too.
    pubDate = models.DateTimeField(null=True,blank=True)
    last_build_date = models.DateTimeField(null=True,blank=True)
    link = models.URLField(null=True,blank=True)
    itunes_subtitle = models.TextField(null=True,blank=True)
    itunes_keywords = models.TextField(null=True, blank=True)
    itunes_image = models.CharField(max_length=400)
    category = models.ManyToManyField(Category)
    podcast_generator = models.ForeignKey(Generator,on_delete=models.CASCADE,null=True)
    podcast_author = models.ForeignKey(PodcastAuthor,on_delete=models.CASCADE)
    podcast_image = models.OneToOneField(Image,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.title}"