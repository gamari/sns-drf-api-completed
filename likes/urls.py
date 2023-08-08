from django.urls import path

from .views import LikeCreateDestroyAPIView

urlpatterns = [
    path("<uuid:post_id>/", LikeCreateDestroyAPIView.as_view()),
]
