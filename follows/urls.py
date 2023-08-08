from django.urls import path
from .views import FollowUserView

urlpatterns = [
    path("follow/<str:user_id>/", FollowUserView.as_view(), name="follow-user"),
]
