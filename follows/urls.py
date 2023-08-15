from django.urls import path
from .views import FollowUserView, FollowerListView, FollowingListView, UnfollowUserView

urlpatterns = [
    path("follow/<str:user_id>/", FollowUserView.as_view()),
    path("unfollow/<str:user_id>/", UnfollowUserView.as_view()),
    path("followings/<str:user_id>/", FollowingListView.as_view()),
    path("followers/<str:user_id>/", FollowerListView.as_view()),
]
