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
