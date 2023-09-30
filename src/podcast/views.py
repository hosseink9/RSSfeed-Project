from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.auth import JwtAuthentication
from .models import Podcast
from episode.models import Episode
from .serializer import PodcastSerializer
from .utils import Parser
from feedback.serializer import LikeSerializer, CommentSerializer, PlaylistSerializer
from feedback.models import Like, Comment, Playlist

from .tasks import save_episode, update_task


class PodcastListView(APIView):
    def get(self, request):
        query = Podcast.objects.all()
        ser_data = PodcastSerializer(instance=query, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class AddPodcastView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAdminUser]

    def post(self, request):
        file = request.FILES["xml"]
        file = file.read()
        save_episode.delay(file)
        return Response({"message":"Rss file save in database successfully."}, status.HTTP_201_CREATED)


class UpdatePodcastView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        file = request.FILES["xml"]
        file = file.read()
        update_task.delay(file)
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

