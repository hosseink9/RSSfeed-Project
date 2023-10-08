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
        if not data:
            logger.error("URL is Invalid")
            raise Response({'message':'URL is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
        save_podcast.delay(data)
        logger.info('Give podcast for parsing')
        return Response({"message":"Rss file save in database successfully."}, status.HTTP_201_CREATED)


class UpdatePodcastView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = request.data['xml']
        if not data:
            logger.error('xml file is invalid')
            raise Response({'message':'xml is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
        update_podcast.delay(data)
        logger.info("Check podcast for updating")
        return Response({"message":"xml is going to update"}, status.HTTP_201_CREATED)


class LikeView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        print(request.user)
        like_serializer = LikeSerializer(data = request.data)
        if not like_serializer.is_valid():
            logger.error("Like Serializer is Invalid!!")
            return Response(like_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if like_serializer.validated_data.get('model') == "podcast":
            podcast = Podcast.objects.get(id = like_serializer.validated_data.get("model_id"))
            if podcast:
                like = Like(content_object = podcast, account = request.user)
                like.save()
                logger.info("Like on podcast is registered")
            else:
                logger.error("Podcast is invalid!!")
                return Response({'message':'Podcast is invalid!'},status=status.HTTP_400_BAD_REQUEST)
        elif like_serializer.validated_data.get('model') == "episode":
            episode = Episode.objects.get(id = like_serializer.validated_data.get("model_id"))
            if episode:
                like = Like(content_object = episode, account = request.user)
                like.save()
                logger.info("Like on episode is registered")
            else:
                logger.error("Episode is invalid!!")
                return Response({'message':'Episode is invalid!'},status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error('Your model is invalid!')
            return Response({'message':'Your model is invalid!'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message":"success"}, status=status.HTTP_201_CREATED)


class CommentView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        print(request.user)
        comment_serializer = CommentSerializer(data = request.data)
        if not comment_serializer.is_valid():
            logger.error("Comment Serializer is Invalid!!")
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if comment_serializer.validated_data.get('model')=="podcast":
            podcast = Podcast.objects.get(id = comment_serializer.validated_data.get("model_id"))
            if podcast:
                comment = Comment(content_object = podcast, account = request.user, text = comment_serializer.validated_data.get("text"))
                comment.save()
                logger.info("Comment on podcast is registered")
            else:
                logger.error("Podcast is invalid!!")
                return Response({'message':'Podcast is invalid!'},status=status.HTTP_400_BAD_REQUEST)
        elif comment_serializer.validated_data.get('model') == "episode":
            episode = Episode.objects.get(id = comment_serializer.validated_data.get("model_id"))
            if episode:
                comment = Comment(content_object = episode, account = request.user, text = comment_serializer.validated_data.get("text"))
                comment.save()
                logger.info("Comment on episode is registered")
            else:
                logger.error("Episode is invalid!!")
                return Response({'message':'Episode is invalid!'},status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error('Your model is invalid!')
            return Response({'message':'Your model is invalid!'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message":"success"}, status=status.HTTP_201_CREATED)


class PlaylistView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        DATA =  request.data.copy()
        DATA['account'] = request.user.id
        DATA.pop("playlist")
        playlist_serializer = PlaylistSerializer(data = DATA, partial = True ,instance=Playlist.objects.get(id=request.data.get("playlist")))
        if not playlist_serializer.is_valid():
            logger.error("Playlist Serializer is Invalid!!")
            return Response(playlist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        playlist_serializer.save()
        logger.info("Item is add to playlist!")
        return Response(data={"message":"success"}, status=status.HTTP_201_CREATED)

