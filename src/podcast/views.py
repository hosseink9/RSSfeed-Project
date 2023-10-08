from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from podcast.models import Podcast
from users.auth import JwtAuthentication
import logging

from episode.tasks import update_podcast
from episode.models import Episode
from .serializer import PodcastSerializer, PodcastUrlSerializer
from feedback.serializer import LikeSerializer, CommentSerializer, PlaylistSerializer
from feedback.models import Like, Comment, Playlist

from .tasks import save_podcast

logger = logging.getLogger('django_API')

class PodcastListView(APIView):
    def get(self, request):
        query = Podcast.objects.all()
        ser_data = PodcastSerializer(instance=query, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class AddPodcastUrlView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAdminUser]

    def post(self,request):
        serializer = PodcastUrlSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Podcast Serializer is Invalid!!")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        logger.info('Give podcast URL')
        return Response({'message': "URL is saved"}, status=status.HTTP_201_CREATED)

class AddPodcastView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAdminUser]

    def post(self, request):
        data = request.data['url']
        save_podcast.delay(data)
        return Response({"message":"Rss file save in database successfully."}, status.HTTP_201_CREATED)


class UpdatePodcastView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = request.data['xml']
        update_podcast.delay(data)
        return Response({"message":"xml is going to update"}, status.HTTP_201_CREATED)


class LikeView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        print(request.user)
        like_serializer = LikeSerializer(data = request.data)
        like_serializer.is_valid(raise_exception=True)
        if like_serializer.validated_data.get('model') == "podcast":
            podcast = Podcast.objects.get(id = like_serializer.validated_data.get("model_id"))
            if podcast:
                like = Like(content_object = podcast, account = request.user)
                like.save()
        elif like_serializer.validated_data.get('model') == "episode":
            episode = Episode.objects.get(id = like_serializer.validated_data.get("model_id"))
            if episode:
                like = Like(content_object = episode, account = request.user)
                like.save()
        return Response(data={"message":"success"}, status=status.HTTP_201_CREATED)


class CommentView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        print(request.user)
        comment_serializer = CommentSerializer(data = request.data)
        comment_serializer.is_valid(raise_exception=True)
        if comment_serializer.validated_data.get('model')=="podcast":
            podcast = Podcast.objects.get(id = comment_serializer.validated_data.get("model_id"))
            if podcast:
                comment = Comment(content_object = podcast, account = request.user, text = comment_serializer.validated_data.get("text"))
                comment.save()
        elif comment_serializer.validated_data.get('model') == "episode":
            episode = Episode.objects.get(id = comment_serializer.validated_data.get("model_id"))
            if episode:
                comment = Comment(content_object = episode, account = request.user, text = comment_serializer.validated_data.get("text"))
                comment.save()
        return Response(data={"message":"success"}, status=status.HTTP_201_CREATED)


class PlaylistView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        DATA =  request.data.copy()
        DATA['account'] = request.user.id
        DATA.pop("playlist")
        playlist_serializer = PlaylistSerializer(data = DATA, partial = True ,instance=Playlist.objects.get(id=request.data.get("playlist")))
        playlist_serializer.is_valid(raise_exception=True)
        playlist_serializer.save()
        return Response(data={"message":"success"}, status=status.HTTP_201_CREATED)

