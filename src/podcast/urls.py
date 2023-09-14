from django.urls import path
from .views import PodcastListView, AddPodcastView

urlpatterns = [
    path("podcasts/", PodcastListView.as_view(), name="podcasts"),
    path("add_podcast/", AddPodcastView.as_view(),name='add_podcast')
]