import logging

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    IntegerField,
    SerializerMethodField,
    PrimaryKeyRelatedField,
)

from accounts.serializers import AccountSerializer

from .models import Post, PostImage

logger = logging.getLogger(__name__)

class PostImageSerializer(ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("id", "image")


class BasePostSerializer(ModelSerializer):
    author = AccountSerializer(read_only=True)
    is_liked = SerializerMethodField()
    is_reposted = SerializerMethodField()

    def _get_user_from_context(self):
        return self.context.get("request", {}).user

    def get_is_liked(self, obj):
        user = self._get_user_from_context()
        if user and user.is_authenticated:
            return obj.is_liked_by_user(user)
        return False

    def get_is_reposted(self, obj):
        user = self._get_user_from_context()
        if user and user.is_authenticated:
            return obj.is_reposted(user)
        return False


class RepostSerializer(BasePostSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "author",
            "created_at",
            "updated_at",
            "likes_count",
            "is_liked",
            "is_reposted",
            "images",
            "reposts_count"
        ]
        depth = 1


class ReplySerializer(BasePostSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "author",
            "created_at",
            "updated_at",
            "likes_count",
            "is_liked",
            "is_reposted",
            "images",
            "reposts_count"
        ]
        depth = 1


class PostSerializer(BasePostSerializer):
    content = CharField(max_length=200, allow_blank=True, required=False)
    likes_count = IntegerField(read_only=True)
    images = PostImageSerializer(many=True, required=False)
    replies_count = IntegerField(read_only=True)
    repost_of = RepostSerializer(read_only=True)
    reply_to = PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "created_at",
            "updated_at",
            "author",
            "images",
            "likes_count",
            "is_liked",
            "repost_of",
            "reposts_count",
            "is_reposted",
            "reply_to",
            "replies_count",
        ]
        depth = 1

    def create(self, validated_data):
        user = self._get_user_from_context()
        images_data = validated_data.pop("images", [])
        logger.debug(f"User from context: {user}")
        logger.debug(f"Images data: {images_data}")
        print(images_data)

        post = Post.objects.create(author=user, **validated_data)

        if "repost_of" not in validated_data:
            print(images_data[0])
            post_image_instances = [
                PostImage.objects.create(**image_data) for image_data in images_data
            ]
            print(post_image_instances[0])
            post.images.set(post_image_instances)

        return post

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.reply_to:
            data["reply_to"] = ReplySerializer(
                instance.reply_to, context={"request": self.context["request"]}
            ).data
        return data
