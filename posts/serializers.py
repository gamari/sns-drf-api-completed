from rest_framework.serializers import ModelSerializer, CharField

from accounts.serializers import AccountSerializer

from .models import Post


class PostSerializer(ModelSerializer):
    author = AccountSerializer(read_only=True)
    content = CharField(max_length=200)

    class Meta:
        model = Post
        fields = ["id", "content", "created_at", "updated_at", "author"]

    def create(self, validated_data):
        user = self.context["request"].user
        post = Post.objects.create(author=user, **validated_data)

        return post
