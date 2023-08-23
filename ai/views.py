from datetime import datetime, timedelta
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.models import Account

from ai.services import generate_tweets
from posts.models import Post

class GenerateTweetsView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        tweets = generate_tweets()
        print(tweets)
        for tweet in tweets:
            ai = Account.objects.filter(is_ai=True).order_by('?').first()
            
            post = Post.objects.create(
               author=ai,
               content="test"
            )

            random_days = random.randint(0, 6)
            random_date = datetime.now() - timedelta(days=random_days)

            post.created_at = random_date
            post.save()
        return Response({"dettail": "ok"})