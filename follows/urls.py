from django.urls import path
from .views import FollowUserView, UnfollowUserView

urlpatterns = [
    path("follow/<str:user_id>/", FollowUserView.as_view()),
    path("unfollow/<str:user_id>/", UnfollowUserView.as_view()),
]
