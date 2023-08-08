from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response

from likes.models import Like
from posts.models import Post


class LikeCreateDestroyAPIView(CreateAPIView, DestroyAPIView):
    queryset = Like.objects.all()

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        user = request.user

        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            return Response(
                {"detail": "既にいいねしています"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "いいねに成功しました"})

    def delete(self, request, post_id):
        post = Post.objects.get(id=post_id)
        user = request.user

        like = Like.objects.filter(user=user, post=post).first()
        if like:
            like.delete()
            return Response({"message": "いいね解除に成功しました。"})
        else:
            return Response(
                {"detail": "いいね解除に失敗しました"},
                status=status.HTTP_400_BAD_REQUEST,
            )
