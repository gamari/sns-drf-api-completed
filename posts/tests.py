from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Post


class PostListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/posts/"
        self.user = get_user_model()

        # テストユーザーと投稿を作成
        self.user1 = self.user.objects.create_user(
            username="user1",
            user_id="user1_id",
            email="user1@example.com",
            password="testpassword",
        )
        self.user2 = self.user.objects.create_user(
            username="user2",
            user_id="user2_id",
            email="user2@example.com",
            password="testpassword",
        )

        self.post1 = Post.objects.create(
            author=self.user1, content="This is a test post."
        )
        self.post2 = Post.objects.create(
            author=self.user1, content="This is another test post.", reply_to=self.post1
        )
        self.post3 = Post.objects.create(
            author=self.user2, content="This is a third test post."
        )

    def test_get_all_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_filter_posts_by_user_id(self):
        response = self.client.get(self.url, {"user_id": self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_filter_posts_by_reply_to(self):
        response = self.client.get(self.url, {"reply_to": self.post1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
