from django.db import models
from accounts.models import Account


class Follow(models.Model):
    follower = models.ForeignKey(
        Account, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        Account, related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
