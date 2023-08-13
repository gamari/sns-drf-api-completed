from django.core.management.base import BaseCommand
from accounts.models import Account


class Command(BaseCommand):
    help = "テストユーザー作成コマンド"

    def add_arguments(self, parser):
        parser.add_argument(
            "number_of_users", type=int, help="Number of test users to be created"
        )

    def handle(self, *args, **kwargs):
        number_of_users = kwargs["number_of_users"]

        for i in range(number_of_users):
            temp = f"test{i+1}"
            email = f"{temp}@example.com"
            username = f"{temp}"
            password = f"{temp}"
            user_id = f"{temp}"
            try:
                Account.objects.create_user(
                    email=email, username=username, password=password, user_id=user_id
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created user {username}")
                )
            except:
                pass
