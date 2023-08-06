from rest_framework.serializers import ModelSerializer

from .models import Account

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'user_id', 'email', 'username', 'password', 'profile_image']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_id = validated_data.pop('user_id')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        account = Account.objects.create_user(email=email, username=username, password=password, user_id=user_id, **validated_data)
        return account

class MeSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'user_id', 'email', 'username', 'profile_image']