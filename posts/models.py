from django.db import models
from django.contrib.auth import get_user_model
import uuid


class PostImage(models.Model):
    image = models.ImageField(upload_to="post_images/")


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, help_text="投稿者"
    )
    content = models.TextField(max_length=10000)
    images = models.ManyToManyField(PostImage, blank=True)
    reply_to = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def likes_count(self):
        return self.like_set.count()

    @property
    def replies_count(self):
        return self.replies.count()

    def is_liked_by_user(self, user):
        return self.like_set.filter(user=user).exists()

    def __str__(self) -> str:
        return f"[{self.id}]{self.content}"
