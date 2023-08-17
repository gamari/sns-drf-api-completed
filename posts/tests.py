from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post

User = get_user_model()

class RepliedPostListAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = get_user_model().objects.create_user(username="testuser", user_id="1", email="test1@example.com", password="testpassword123")
        self.user2 = get_user_model().objects.create_user(username="testuser2", user_id="2", email="test2@example.com", password="testpassword123")

        self.post1 = Post.objects.create(content="post1", author=self.user1)
        self.post2 = Post.objects.create(content="reply to post1", reply_to=self.post1, author=self.user1)
        self.post3 = Post.objects.create(content="post3", author=self.user1)

    def test_api_endpoint(self):
        # ユーザーをログインさせる
        self.client.login(username="testuser", password="testpassword123")

        response = self.client.get(reverse('replied-posts') + f'?user_id={self.user1.id}')
        results = response.data["results"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 1)
