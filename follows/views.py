from follows.models import Follow
from follows.serializers import FollowSerializer

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Account


class FollowUserView(CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        following_user_id = self.kwargs.get("user_id")
        following = Account.objects.get(user_id=following_user_id)
        serializer.save(follower=self.request.user, following=following)
