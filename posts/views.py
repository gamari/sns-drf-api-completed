from django.db.models import Q

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer, RepostSerializer


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return obj.author == request.user


class PostRetrieveDestroyView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("images")
        user_id = self.request.query_params.get("user_id", None)
        if user_id is not None:
            queryset = queryset.filter(author__id=user_id)

        return queryset.order_by("-created_at")

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        if self.request.method == "DELETE":
            return [IsOwnerOrReadOnly()]

        return [IsAuthenticated()]


class BasePostListView(ListAPIView):
    serializer_class = PostSerializer

    def get_user_id(self):
        return self.request.query_params.get("user_id", None)
    
    def get_search_word(self):
        return self.request.query_params.get("word", None)

    def filter_by_user_id(self, queryset, user_id):
        if user_id:
            queryset = queryset.filter(author__id=user_id)
        return queryset

    def filter_by_reply_to(self, queryset, reply_to_id):
        if reply_to_id:
            queryset = queryset.filter(reply_to=reply_to_id)
        return queryset

    
    def filter_by_search(self, queryset, keyword):
        if keyword:
            queryset = queryset.filter(
                Q(content__icontains=keyword)
            )
        return queryset

    def filter_by_created_at(self ,queryset, start_date):
        # TODO 使う
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset

    def order_queryset_by_created_at_desc(self, queryset):
        return queryset.order_by("-created_at")


class PostListCreateView(BasePostListView, ListCreateAPIView):
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("images").select_related("repost_of")

        queryset = self.filter_by_user_id(queryset, self.get_user_id())
                                    
        queryset = self.filter_by_reply_to(queryset, self.request.query_params.get("reply_to", None))

        queryset = self.filter_by_search(queryset, self.get_search_word())

        return self.order_queryset_by_created_at_desc(queryset)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]


class LikedPostListAPIView(BasePostListView):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.get_user_id()

        if not user_id:
            return []

        liked_posts = self.queryset.filter(like__user_id=user_id)
        return self.order_queryset_by_created_at_desc(liked_posts)


class MediaPostListAPIView(BasePostListView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.get_user_id()

        if not user_id:
            return []

        filtered_posts = Post.objects.filter(images__isnull=False, author=user_id)
        return self.order_queryset_by_created_at_desc(filtered_posts)


class RepliedPostListAPIView(BasePostListView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.get_user_id()

        if not user_id:
            return []

        replied_posts = Post.objects.filter(reply_to__isnull=False, author=user_id)
        return self.order_queryset_by_created_at_desc(replied_posts)

class FollowingPostsListAPIView(BasePostListView):
    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.all()
        following_users = user.following.values_list('following', flat=True)
        return queryset.filter(author__in=following_users)



class RepostAPIView(APIView):
    MESSAGE_ALREADY_REPOSTED = {"message": "既にリポストしてます。"}
    MESSAGE_POST_NOT_FOUND = {"message": "ポストが存在しません。"}
    MESSAGE_REPOST_NOT_FOUND = {"message": "リポストが見つかりません。"}
    MESSAGE_REPOST_REMOVED = {"message": "リポストを解除しました。"}

    def _get_original_post_or_repost(self, pk):
        post = Post.objects.get(pk=pk)
        return post.repost_of if post.repost_of else post

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            if Post.objects.filter(repost_of=post, author=request.user).exists():
                return Response(
                    self.MESSAGE_ALREADY_REPOSTED, status=status.HTTP_400_BAD_REQUEST
                )

            repost = post.create_repost(request.user)
            serializer = RepostSerializer(instance=repost, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response(
                self.MESSAGE_POST_NOT_FOUND, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            if post.remove_repost(request.user):
                serializer = RepostSerializer(
                    instance=post, context={"request": request}
                )

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    self.MESSAGE_REPOST_NOT_FOUND, status=status.HTTP_404_NOT_FOUND
                )

        except Post.DoesNotExist:
            return Response(
                self.MESSAGE_POST_NOT_FOUND, status=status.HTTP_404_NOT_FOUND
            )
