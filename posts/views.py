from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Like, Post
from .serializers import PostSerializer


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]
    

# 良いね処理
class LikeCreateDestroyAPIView(CreateAPIView, DestroyAPIView):
    queryset = Like.objects.all()

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        user = request.user

        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            return Response({"detail": "You've already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Liked successfully."})

    def delete(self, request, post_id):
        post = Post.objects.get(id=post_id)
        user = request.user

        like = Like.objects.filter(user=user, post=post).first()
        if like:
            like.delete()
            return Response({"message": "Unliked successfully."})
        else:
            return Response({"detail": "You haven't liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)