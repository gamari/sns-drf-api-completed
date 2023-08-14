from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission

from .models import Post
from .serializers import PostSerializer, RepostSeializer

from rest_framework.generics import RetrieveDestroyAPIView


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


class RepostAPIView(APIView):
    def post(self, request, pk):
        # TODO 判定ロジックを行う
        # TODO リツイートのリツイートを対象にする
        original_post = Post.objects.get(pk=pk)
        user = request.user
        target = Post.objects.get(pk=original_post.id, author=user)
        print(target)
        if target:
            return Response({"message": "既にリポストしてます。"}, 400)
        repost = Post.objects.create(repost_of=original_post, author=request.user)
        serializer = RepostSeializer(instance=repost)
        return Response(serializer.data, 200)
