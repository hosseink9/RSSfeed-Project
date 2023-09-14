from django.contrib import admin
from .models import PodcastAuthor, EpisodeAuthor

admin.site.register(PodcastAuthor)
admin.site.register(EpisodeAuthor)
