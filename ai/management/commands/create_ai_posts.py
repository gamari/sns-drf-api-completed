from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from accounts.models import Account
import random
from faker import Faker

from posts.models import Post

fake = Faker('ja_JP')

class Command(BaseCommand):
    help = 'AIユーザーを3ユーザー作成する。'

    def handle(self, *args, **kwargs):
        for _ in range(3):
            ai_users = Account.objects.filter(is_ai=True)
            if not ai_users.exists():
                self.stdout.write(self.style.ERROR('No AI users found.'))
                return

            ai_user = random.choice(ai_users)
            
            post_content = fake.text(max_nb_chars=200)  
            post = Post(
                author=ai_user,
                content=post_content
            )
            post.save()

            random_minutes = random.randint(0, 3 * 24 * 60)
            post.created_at = datetime.now() + timedelta(minutes=random_minutes)
            post.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully created a post by AI user {ai_user.username}'))
