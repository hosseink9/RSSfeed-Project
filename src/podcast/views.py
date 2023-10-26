from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from podcast.models import Podcast
from users.auth import JwtAuthentication
from django.utils.translation import gettext as _

from episode.tasks import update_podcast, update_all_podcast
from episode.models import Episode
from .serializer import PodcastSerializer, PodcastUrlSerializer
from feedback.serializer import LikeSerializer, CommentSerializer, PlaylistSerializer
from feedback.models import Like, Comment, Playlist

from .tasks import save_podcast


class PodcastListView(APIView):
    def get(self, request):
        query = Podcast.objects.all()
        serializer_data = PodcastSerializer(instance=query, many=True)
        # print(serializer_data.get('title'))
        message = _("All podcasts")
        return Response((serializer_data.data,message), status=status.HTTP_200_OK)


class AddPodcastUrlView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAdminUser]

    def post(self,request):
        serializer = PodcastUrlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response( _("URL is saved"), status=status.HTTP_201_CREATED)

class AddPodcastView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAdminUser]

    def post(self, request):
        data = request.data['url']
        if not data:
            raise Response(_('URL is invalid!'), status=status.HTTP_400_BAD_REQUEST)
        save_podcast.delay(data)
        return Response({"message":_("Rss file save in database successfully.")}, status.HTTP_201_CREATED)


class UpdatePodcastView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request=None):
        data = request.data.get('xml')
        if data == None:
            update_all_podcast.delay()
            return Response({"message":_("All urls are going to update")}, status.HTTP_201_CREATED)
            # raise Response(_('xml is invalid!'), status=status.HTTP_400_BAD_REQUEST)
        update_podcast.delay(data)
        return Response({"message":_("xml is going to update")}, status.HTTP_201_CREATED)


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
        return Response(data={"message":_("success")}, status=status.HTTP_201_CREATED)


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
        return Response(data={"message":_("success")}, status=status.HTTP_201_CREATED)


class PlaylistView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        DATA =  request.data.copy()
        DATA['account'] = request.user.id
        DATA.pop("playlist")
        playlist_serializer = PlaylistSerializer(data = DATA, partial = True ,instance=Playlist.objects.get(id=request.data.get("playlist")))
        playlist_serializer.is_valid(raise_exception=True)
        playlist_serializer.save()
        return Response(data={"message":_("success")}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        query = Playlist.objects.filter(account=user)
        playlist_serializer = PlaylistSerializer(instance=query, many=True)
        return Response(playlist_serializer.data, status=status.HTTP_200_OK)



class RecommendationView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request):
        categories = Playlist.objects.filter(account=request.user).values_list("podcasts__category__name")
        categories = list(map(lambda item:item[0], categories))
        recommended_podcast = Podcast.objects.filter(category__name__in=categories)[:10]
        serializer = PodcastSerializer(instance=recommended_podcast, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

