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

