from rest_framework.serializers import ModelSerializer, SerializerMethodField

from follows.models import Follow

from .models import Account


class AccountSerializer(ModelSerializer):
    is_following = SerializerMethodField()
    followers_count = SerializerMethodField()
    following_count = SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            "id",
            "user_id",
            "email",
            "bio",
            "username",
            "password",
            "profile_image",
            "is_following",
            "followers_count",
            "following_count",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "email": {"write_only": True, "required": False},
            "user_id": {"required": False},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user_id = validated_data.pop("user_id")
        email = validated_data.pop("email")
        username = validated_data.pop("username")
        account = Account.objects.create_user(
            email=email,
            username=username,
            password=password,
            user_id=user_id,
            **validated_data
        )
        return account

    def update(self, instance, validated_data):
        validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def get_is_following(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return Follow.objects.filter(follower=user, following=obj).exists()

    def get_followers_count(self, obj):
        return obj.get_followers_count()

    def get_following_count(self, obj):
        return obj.get_following_count()
