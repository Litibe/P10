from rest_framework.serializers import ModelSerializer, ValidationError, EmailField, CharField
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from authentication.models import User


class UserSerializer(ModelSerializer):
    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = CharField(write_only=True, required=True,
                         validators=[validate_password])

    class Meta:
        model = User
        fields = ('email', 'password',
                  'last_name', 'first_name', 'id')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
