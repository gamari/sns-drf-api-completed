from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.serializers import AccountSerializer
from accounts.models import Account
from follows.models import Follow
from follows.serializers import FollowSerializer


class FollowingListView(ListAPIView):
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        following_ids = Follow.objects.filter(follower__id=user_id).values_list(
            "following", flat=True
        )
        return Account.objects.filter(id__in=following_ids)


class FollowerListView(ListAPIView):
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        followers_ids = Follow.objects.filter(following__id=user_id).values_list(
            "follower", flat=True
        )

        return Account.objects.filter(id__in=followers_ids)


class BaseFollowView:
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_following_user(self):
        following_user_id = self.kwargs.get("user_id")
        return Account.objects.get(pk=following_user_id)


class FollowUserView(BaseFollowView, CreateAPIView):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        following = self.get_following_user()
        serializer.save(follower=self.request.user, following=following)


class UnfollowUserView(BaseFollowView, DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        follower = self.request.user
        following = self.get_following_user()
        return self.queryset.get(follower=follower, following=following)
