from django.urls import path
from .views import PodcastListView, PodcastCreateView

urlpatterns = [
    path("podcasts/", PodcastListView.as_view(), name="podcasts"),
    path("create_podcast/", PodcastCreateView.as_view(),name='create')
]