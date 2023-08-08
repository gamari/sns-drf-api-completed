from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    IntegerField,
    SerializerMethodField,
)

from accounts.serializers import AccountSerializer

from .models import Post, PostImage


class PostImageSerializer(ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("id", "image")


class PostSerializer(ModelSerializer):
    author = AccountSerializer(read_only=True)
    content = CharField(max_length=200)
    likes_count = IntegerField(read_only=True)
    is_liked = SerializerMethodField()
    images = PostImageSerializer(many=True, required=False)

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
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        images_data = validated_data.pop("images", [])
        post = Post.objects.create(author=user, **validated_data)

        post_image_instances = []
        for image_data in images_data:
            post_image = PostImage.objects.create(**image_data)
            post_image_instances.append(post_image)

        post.images.set(post_image_instances)

        return post

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.is_liked_by_user(user)
        return False
