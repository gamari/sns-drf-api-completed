from django.urls import path

from .views import (
    LikedPostListAPIView,
    MediaPostListAPIView,
    PostListCreateView,
    PostRetrieveDestroyView,
    RepostAPIView,
)

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("repost/<uuid:pk>/", RepostAPIView.as_view()),
    path("liked/", LikedPostListAPIView.as_view()),
    path("media/", MediaPostListAPIView.as_view()),
    path("<uuid:pk>/", PostRetrieveDestroyView.as_view()),
]
