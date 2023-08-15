from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    IntegerField,
    SerializerMethodField,
    PrimaryKeyRelatedField,
)

from accounts.serializers import AccountSerializer

from .models import Post, PostImage


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
        ]
        depth = 2


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
            "likes_count",
            "is_liked",
            "images",
            "reply_to",
            "repost_of",
            "replies_count",
            "is_reposted",
        ]
        depth = 2

    def create(self, validated_data):
        user = self._get_user_from_context()
        images_data = validated_data.pop("images", [])
        print(validated_data)
        post = Post.objects.create(author=user, **validated_data)

        if "repost_of" not in validated_data:
            post_image_instances = [
                PostImage.objects.create(**image_data) for image_data in images_data
            ]
            post.images.set(post_image_instances)

        return post
