from rest_framework.serializers import ModelSerializer

from authentication.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_name', 'first_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self, data):
        print(data)
        new_user = User(first_name=data.get("first_name"), last_name=data.get(
            "last_name"), email=data.get("email"))
        new_user.set_password(data.get('password'))
        new_user.save()
        return new_user
