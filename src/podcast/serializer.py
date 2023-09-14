from rest_framework.serializers import ModelSerializer
from .models import Podcast


class PodcastSerializer(ModelSerializer):
    class Meta:
        model = Podcast
        fields = "__all__"
