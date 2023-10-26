from rest_framework import serializers
from .models import Playlist
from podcast.serializer import PodcastSerializer
from episode.serializers import EpisodeSerializer

class LikeSerializer(serializers.Serializer):
    model = serializers.CharField(max_length = 50)
    model_id = serializers.IntegerField()


class CommentSerializer(serializers.Serializer):
    model = serializers.CharField(max_length = 50)
    model_id = serializers.IntegerField()
    text = serializers.CharField()


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['title','description','podcasts','episodes']
        optional_fields = ['account']
        unique_together = ['account', 'title']

    def create(self, validated_data):
        request=self.context.get('request')
        podcast_list = validated_data.pop('podcasts')
        episode_list = validated_data.pop('episodes')

        instance = Playlist.objects.create(**validated_data, account=request.user)
        for podcast in podcast_list:
            instance.podcasts.add(podcast)
        for episode in episode_list:
            instance.episodes.add(episode)
        return instance


    def update(self, instance, validated_data):
        for podcast in validated_data.get("podcasts"):
            instance.podcasts.add(podcast)
        for episode in validated_data.get("episodes"):
            instance.episodes.add(episode)
        instance.save()
        return instance

