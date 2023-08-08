from django.db import models
from django.contrib.auth import get_user_model
import uuid


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, help_text="投稿者"
    )
    content = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def likes_count(self):
        return self.like_set.count()
    
    def is_liked_by_user(self, user):
        return self.like_set.filter(user=user).exists()

    def __str__(self) -> str:
        return f"[{self.id}]{self.content}"

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']