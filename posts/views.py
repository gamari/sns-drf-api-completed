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


# TODO BaseListAPIViewを作る


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("images").select_related("repost_of")

        user_id = self.request.query_params.get("user_id", None)
        if user_id:
            queryset = queryset.filter(author__id=user_id)

        reply_to_id = self.request.query_params.get("reply_to", None)

        if reply_to_id:
            queryset = queryset.filter(reply_to=reply_to_id)

        return queryset.order_by("-created_at")

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]


class LikedPostListAPIView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id", None)

        if not user_id:
            return []

        # TODO Likeの作成日順で並び替えたい
        print(user_id)
        liked_posts = queryset.filter(like__user_id=user_id).order_by("-created_at")

        return liked_posts


class MediaPostListAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id", None)

        if not user_id:
            return []

        filtered_posts = Post.objects.filter(images__isnull=False).filter(
            author=user_id
        )

        return filtered_posts.order_by("-created_at")


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
