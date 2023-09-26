from django.urls import path
from .views import PodcastListView, AddPodcastView, LikeView, CommentView, PlaylistView, UpdatePodcastView

urlpatterns = [
    path("podcasts/", PodcastListView.as_view(), name="podcasts"),
    path("add_podcast/", AddPodcastView.as_view(),name='add_podcast'),
    path("like/", LikeView.as_view(),name='like'),
    path("comment/", CommentView.as_view(),name='comment'),
    path("playlist/", PlaylistView.as_view(),name='playlist'),
    path("update/", UpdatePodcastView.as_view(),name='update'),
]