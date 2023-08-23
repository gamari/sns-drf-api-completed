from django.core.management.base import BaseCommand
from accounts.models import Account
import random
import string

# TODO アイコンを決めたい

class Command(BaseCommand):
    help = 'AIユーザーを10ユーザー作成する。'

    def handle(self, *args, **kwargs):
        for _ in range(10):
            # TODO ランダム関数を作る
            user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
            email = f"{user_id}@aiuser.com"
            username = f"AI_{user_id}"
            Account.objects.create(
                user_id=user_id,
                email=email,
                username=username,
                is_ai=True
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created AI user {username}'))
