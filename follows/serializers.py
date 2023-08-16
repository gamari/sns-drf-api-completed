from rest_framework import serializers

from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.HiddenField(default=serializers.CurrentUserDefault())
    following = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = ("follower", "following")
        extra_kwargs = {"following": {"required": False}}
