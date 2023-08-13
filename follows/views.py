from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from follows.models import Follow
from follows.serializers import FollowSerializer
from .models import Account


class FollowUserView(CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

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
