from django.urls import path
from .views import PodcastListView, AddPodcastView, LikeView, CommentView, AddToPlaylistView, UpdatePodcastView, AddPodcastUrlView,RecommendationView, PlaylistView

app_name = 'podcast'

urlpatterns = [
    path("podcasts/", PodcastListView.as_view(), name="podcasts"),
    path("add_podcast_url/", AddPodcastUrlView.as_view(), name="podcasts"),
    path("add_podcast/", AddPodcastView.as_view(),name='add_podcast'),
    path("like/", LikeView.as_view(),name='like'),
    path("comment/", CommentView.as_view(),name='comment'),
    path("add_to_playlist/", AddToPlaylistView.as_view(),name='add_to_playlist'),
    path("create_playlist/", PlaylistView.as_view(),name='add_to_playlist'),
    path("recommendation/", RecommendationView.as_view(),name='recommendation'),
    path("update/", UpdatePodcastView.as_view(),name='update'),
]