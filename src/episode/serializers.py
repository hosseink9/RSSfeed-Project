from rest_framework import serializers
from .models import Episode

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['title','guid','itunes_episode_type','itunes_explicit','description','enclosure','link','pubDate','itunes_keywords','itunes_player','episode_podcast','episode_author']