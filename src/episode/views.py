from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Episode
from .serializers import EpisodeSerializer

class EpisodeListView(APIView):
    def get(self, request):
        queryset = Episode.objects.all()
        serializer_data = EpisodeSerializer(queryset, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)


