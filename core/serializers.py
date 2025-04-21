from djoser.serializers import UserSerializer as CurrentUserSerializer, UserCreateSerializer as BaseUserSerializer

from store.models import Customer


class UserCreateSerializer(BaseUserSerializer):
    # def save(self, **kwargs):
    #     user = super().save(**kwargs)
    #     Customer.objects.create(user=user)

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']

class UserSerializer(CurrentUserSerializer):
    class Meta(CurrentUserSerializer.Meta):
        fields = ['id', 'username',
                  'email', 'first_name', 'last_name']