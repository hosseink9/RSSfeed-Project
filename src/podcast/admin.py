from django.contrib import admin
from .models import Podcast, Category, Generator, Image, Owner, PodcastUrl

# Register your models here.
admin.site.register(Podcast)
admin.site.register(Category)
admin.site.register(Generator)
admin.site.register(Image)
admin.site.register(Owner)
admin.site.register(PodcastUrl)