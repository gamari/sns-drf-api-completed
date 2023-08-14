from django.urls import path

from .views import PostListCreateView, PostRetrieveDestroyView, RepostAPIView

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("<uuid:pk>/", PostRetrieveDestroyView.as_view()),
    path("repost/<uuid:pk>/", RepostAPIView.as_view()),
]
