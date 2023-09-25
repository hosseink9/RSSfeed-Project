from rest_framework import serializers
from .models import Like, Comment, Playlist
from podcast.models import Podcast
from episode.models import Episode
from users.models import User


class LikeSerializer(serializers.Serializer):
    model = serializers.CharField(max_length = 50)
    model_id = serializers.IntegerField()
