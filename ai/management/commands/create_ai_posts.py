from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from accounts.models import Account
import random
from faker import Faker

from ai.services import generate_tweets
from posts.models import Post

fake = Faker('ja_JP')

class Command(BaseCommand):
    help = 'AIユーザーを3ユーザー作成する。'

    def handle(self, *args, **kwargs):
        posts = generate_tweets(20)

        for post_item in posts:
            ai_users = Account.objects.filter(is_ai=True)
            if not ai_users.exists():
                self.stdout.write(self.style.ERROR('No AI users found.'))
                return

            ai_user = random.choice(ai_users)
            
            post = Post(
                author=ai_user,
                content=post_item
            )
            post.save()

            random_minutes = random.randint(0, 1 * 24 * 60)
            # random_minutes = random.randint(0, 5)
            post.created_at = datetime.now() + timedelta(minutes=random_minutes)
            post.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully created a post by AI user {ai_user.username}'))
