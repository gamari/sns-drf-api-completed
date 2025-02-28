from django.urls import path

from .views import (
    FollowingPostListAPIView,
    LikedPostListAPIView,
    MediaPostListAPIView,
    PostListCreateView,
    PostRetrieveDestroyView,
    RepostAPIView,
    RepliedPostListAPIView,
)

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("liked/", LikedPostListAPIView.as_view()),
    path("replied/", RepliedPostListAPIView.as_view(), name="replied-posts"),
    path("media/", MediaPostListAPIView.as_view()),
    path("repost/<uuid:pk>/", RepostAPIView.as_view()),
    path("following/", FollowingPostListAPIView.as_view()),
    path("<uuid:pk>/", PostRetrieveDestroyView.as_view()),
]
