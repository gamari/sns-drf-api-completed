from django.urls import path

from .views import LikeCreateDestroyAPIView, PostListCreateView

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("likes/<slug:post_id>/", LikeCreateDestroyAPIView.as_view()),
]
