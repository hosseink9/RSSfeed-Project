from rest_framework.serializers import ModelSerializer
from .models import Like, Comment


class LikeSerializer(ModelSerializer):
    class META:
        model = Like
        fields = ['user','content_type']


class CommentSerializer(ModelSerializer):
    class META:
        model = Comment
        fields = ['user','text','content_type',]