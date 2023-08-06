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

    # TODO 追加
    def __str__(self) -> str:
        return f"[{self.id}]{self.content}"
