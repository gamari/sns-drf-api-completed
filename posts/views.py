from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Post
from .serializers import PostSerializer


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]
