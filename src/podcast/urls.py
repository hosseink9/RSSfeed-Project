from django.urls import path
from .views import PodcastListView, AddPodcastView, LikeView, CommentView, PlaylistView, UpdatePodcastView, AddPodcastUrlView,RecommendationView

app_name = 'podcast'

urlpatterns = [
    path("podcasts/", PodcastListView.as_view(), name="podcasts"),
    path("add_podcast_url/", AddPodcastUrlView.as_view(), name="podcasts"),
    path("add_podcast/", AddPodcastView.as_view(),name='add_podcast'),
    path("like/", LikeView.as_view(),name='like'),
    path("comment/", CommentView.as_view(),name='comment'),
    path("playlist/", PlaylistView.as_view(),name='playlist'),
    path("recommendation/", RecommendationView.as_view(),name='recommendation'),
    path("update/", UpdatePodcastView.as_view(),name='update'),
]