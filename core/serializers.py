from djoser.serializers import UserSerializer as CurrentUserSerializer, UserCreateSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']

class UserSerializer(CurrentUserSerializer):
    class Meta(CurrentUserSerializer.Meta):
        fields = ['id', 'username',
                  'email', 'first_name', 'last_name']