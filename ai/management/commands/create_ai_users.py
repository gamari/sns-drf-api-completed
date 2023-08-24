from django.core.management.base import BaseCommand
from accounts.models import Account
import random
import string
from faker import Faker

fake = Faker('ja_JP')

# TODO アイコンを決めたい
class Command(BaseCommand):
    help = 'AIユーザーを3ユーザー作成する。'

    def handle(self, *args, **kwargs):
        for _ in range(3):
            user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
            email = f"{user_id}@aiuser.com"
            
            username = fake.name()
            
            Account.objects.create(
                user_id=user_id,
                email=email,
                username=username,
                is_ai=True
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created AI user {username}'))
