from rest_framework.serializers import ModelSerializer
from .models import Podcast, PodcastUrl


class PodcastSerializer(ModelSerializer):
    class Meta:
        model = Podcast
        fields = "__all__"


class PodcastUrlSerializer(ModelSerializer):
    class Meta:
        model = PodcastUrl
        fields = ['url','title']
