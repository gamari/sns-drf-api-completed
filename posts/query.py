import datetime
from django.db.models import Q

from posts.models import Post


class PostQueryBuilder(object):
    def __init__(self):
        self.queryset = Post.objects.all()

    def build(self):
        return self.queryset
    
    def prefetch_related(self, target):
        self.queryset.prefetch_related(target)
        return self

    def filter_by_user_id(self, user_id):
        if user_id:
            self.queryset = self.queryset.filter(author__id=user_id)
        return self
    
    def filter_by_created_at(self, created_at):
        if created_at:
            self.queryset = self.queryset.filter(created_at__lte=created_at)
        else:
            now = datetime.now()
            self.queryset = self.queryset.filter(created_at__lte=now)
        return self
    
    def filter_by_word(self, word):
        if word:
            self.queryset = self.queryset.filter(content__icontains=word)
        return self

    def filter_by_reply_to(self, reply_to_id):
        if reply_to_id:
            self.queryset = self.queryset.filter(reply_to=reply_to_id)
        return self

    def filter_by_search(self, keyword):
        if keyword:
            self.queryset = self.queryset.filter(Q(content__icontains=keyword))
        return self

    def filter_by_created_at(self, start_date):
        if start_date:
            self.queryset = self.queryset.filter(created_at__gte=start_date)
        return self

    def filter_by_liked_user(self, user_id):
        self.queryset = self.queryset.filter(like__user_id=user_id)
        return self
    
    def filter_by_media(self, user_id):
        self.queryset = self.queryset.filter(images__isnull=False, author__id=user_id)
        return self

    def filter_by_reply(self, user_id):
        self.queryset = self.queryset.filter(reply_to__isnull=False, author__id=user_id)
        return self

    def filter_by_following_users(self, user):
        following_users = user.following.values_list('following', flat=True)
        self.queryset = self.queryset.filter(author__in=following_users)
        return self

    def order_by_created_at_desc(self):
        self.queryset = self.queryset.order_by("-created_at")
        return self
