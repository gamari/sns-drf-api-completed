from django.db.models import Q

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny,  IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.permissions import IsOwnerOrReadOnly

from posts.query import PostQueryBuilder

from .models import Post
from .serializers import PostSerializer, RepostSerializer





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
    queryset = Post.objects.all()

    def get_user_id(self):
        return self.request.query_params.get("user_id", None)
    
    def get_word(self):
        return self.request.query_params.get("word", None)
    
    def get_search_word(self):
        return self.request.query_params.get("word", None)
    
    def get_reply_to_id(self):
        print(self.request.query_params)
        return self.request.query_params.get("reply_to", None)



class PostListCreateView(BasePostListView, ListCreateAPIView):
    def get_queryset(self):
        builder = PostQueryBuilder()\
            .prefetch_related("images")\
            .filter_by_user_id(self.get_user_id())\
            .filter_by_reply_to(self.get_reply_to_id())\
            .filter_by_word(self.get_word())\
            .order_by_created_at_desc()
        
        return builder.build()    

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

# TODO ここらへんまとめたい
class LikedPostListAPIView(BasePostListView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.get_user_id()

        if not user_id:
            return []

        builder = PostQueryBuilder()\
            .filter_by_liked_user(user_id)\
            .order_by_created_at_desc()
        
        return builder.build()

class MediaPostListAPIView(BasePostListView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.get_user_id()

        if not user_id:
            return []

        builder = PostQueryBuilder()\
            .filter_by_media(user_id)\
            .order_by_created_at_desc()

        return builder.build()

class RepliedPostListAPIView(BasePostListView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.get_user_id()

        if not user_id:
            return []

        print(user_id)
        builder = PostQueryBuilder()\
            .filter_by_reply(user_id)\
            .order_by_created_at_desc()

        return builder.build()

class FollowingPostsListAPIView(BasePostListView):
    def get_queryset(self):
        user = self.request.user

        builder = PostQueryBuilder()\
            .filter_by_following_users(user)\
            .order_by_created_at_desc()

        return builder.build()



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
