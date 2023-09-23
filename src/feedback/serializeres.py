from rest_framework.serializers import ModelSerializer
from .models import Like, Comment


class LikeSerializer(ModelSerializer):
    class META:
        model = Like
        fields = ['user','content_type']
