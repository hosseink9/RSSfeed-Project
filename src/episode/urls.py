from django.urls import path

from .views import EpisodeListView

app_name = 'episode'

urlpatterns = [
    path('episodes/', EpisodeListView.as_view(), name='episode')
]