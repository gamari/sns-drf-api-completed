import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です。")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("管理者ユーザはis_staffがtrueである必要があります。")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("管理者ユーザーはis_superuserがtrueである必要があります")

        return self.create_user(email, username, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(
        max_length=30, unique=True, editable=True, help_text="ユーザーが設定できるID"
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    header_image = models.ImageField(upload_to="headers/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def get_followers_count(self):
        from follows.models import Follow

        return Follow.objects.filter(following=self).count()

    def get_following_count(self):
        from follows.models import Follow

        return Follow.objects.filter(follower=self).count()
