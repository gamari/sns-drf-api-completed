from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountSerializer


# Account単体処理
class AccountRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    # TODO permisonの変更
    permission_classes = [AllowAny]
    serializer_class = AccountSerializer
    lookup_field = "id"


# Account複数処理
class CreateAccountView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            return Response(
                {
                    "user_id": account.user_id,
                    "email": account.email,
                    "username": account.username,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 認証用ユーザー処理
class MeView(APIView):
    def get(self, request):
        serializer = AccountSerializer(request.user, context={"request": request})
        return Response(serializer.data)
