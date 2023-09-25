from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Podcast
from .serializer import PodcastSerializer
from .utils import Parser

# Create your views here.
class PodcastListView(APIView):
    def get(self, request):
        query = Podcast.objects.all()
        ser_data = PodcastSerializer(instance=query, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class AddPodcastView(APIView):
    def post(self, request):
        file = request.FILES["xml"]
        file = file.read()
        Parser(rss_file=file.decode("utf-8"), save=True)
        return Response({"message":"Rss file save in database successfully."}, status.HTTP_201_CREATED)
class LikeView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        print(request.user)
        like_serializer = LikeSerializer(data = request.data)
        like_serializer.is_valid(raise_exception=True)
        if like_serializer.validated_data.get('model')=="podcast":
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

