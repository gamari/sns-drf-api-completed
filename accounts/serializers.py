import re

from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

from follows.models import Follow

from accounts.models import Account


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
    
    def validate_user_id(self, value):
        if len(value) > 20:
            raise ValidationError("user_idは20文字以下である必要があります。")
        if not re.match("^[a-zA-Z0-9!@#$%^&*(),.?\":{}|<>]+$", value):
            raise ValidationError("user_idは半角数字・半角英語・記号のみ可能です。")
        return value

    def validate_username(self, value):
        if len(value) > 5:
            raise ValidationError("usernameは20文字以下である必要があります。")
        return value

    def validate_password(self, value):
        if len(value) > 24:
            raise ValidationError("パスワードは24文字以下である必要があります。")
        if not re.match("^[a-zA-Z0-9!@#$%^&*(),.?\":{}|<>]+$", value):
            raise ValidationError("パスワードは半角数字・半角英語・記号のみ可能です。")
        return value

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

        # TODO bioは0文字でも更新したい
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
