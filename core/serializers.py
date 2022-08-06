from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaserUserSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    # birth_date = serializers.DateField(read_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'first_name', 'last_name',
                  'email', 'username', 'password']


class UserSerializer(BaserUserSerializer):
    class Meta(BaserUserSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
