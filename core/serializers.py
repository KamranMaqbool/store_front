from djoser.serializers import UserSerializer as BaserUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):
    # birth_date = serializers.DateField(read_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'username', 'password']


class UserSerializer(BaserUserSerializer):
    class Meta(BaserUserSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email']