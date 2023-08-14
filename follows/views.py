from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from accounts.serializers import AccountSerializer
from follows.models import Follow
from follows.serializers import FollowSerializer
from .models import Account


class FollowingListView(ListAPIView):
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        following_ids = Follow.objects.filter(follower__id=user_id).values_list(
            "following", flat=True
        )
        print(following_ids)
        return Account.objects.filter(id__in=following_ids)


class FollowUserView(CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        following_user_id = self.kwargs.get("user_id")
        following = Account.objects.get(pk=following_user_id)
        serializer.save(follower=self.request.user, following=following)


class UnfollowUserView(DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        follower = self.request.user
        following_user_id = self.kwargs.get("user_id")
        following = Account.objects.get(pk=following_user_id)
        return self.queryset.get(follower=follower, following=following)
