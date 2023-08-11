from django.urls import path

from .views import PostListCreateView, PostRetrieveDestroyView

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("<uuid:pk>/", PostRetrieveDestroyView.as_view()),
]
