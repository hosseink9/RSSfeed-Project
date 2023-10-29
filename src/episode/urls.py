from django.urls import path

from .views import EpisodeListView, EpisodeView

app_name = 'episode'

urlpatterns = [
    path('episodes/', EpisodeListView.as_view(), name='episode'),
    path('episode_view/<id>', EpisodeView.as_view(), name='episode_view')
]