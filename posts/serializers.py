from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    IntegerField,
    SerializerMethodField,
)

from accounts.serializers import AccountSerializer

from .models import Post


class PostSerializer(ModelSerializer):
    author = AccountSerializer(read_only=True)
    content = CharField(max_length=200)
    likes_count = IntegerField(read_only=True)
    is_liked = SerializerMethodField()

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
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        post = Post.objects.create(author=user, **validated_data)

        return post

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.is_liked_by_user(user)
        return False
