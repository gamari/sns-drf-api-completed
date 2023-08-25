import logging
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
        logger = logging.getLogger('all')
        logger.debug("test")
        tweets = generate_tweets()
        logger.info(tweets)
        for tweet in tweets:
            ai = Account.objects.filter(is_ai=True).order_by('?').first()
            
            post = Post.objects.create(
               author=ai,
               content=tweet
            )

            random_days = random.randint(0, 6)
            random_date = datetime.now() - timedelta(minutes=random_days)

            post.created_at = random_date
            post.save()
        return Response({"dettail": "ok"})