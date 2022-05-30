from rest_framework.serializers import ModelSerializer
from ..models import User

class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)
        user = User(
            email=email
        )
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'last_login', 'password']
        extra_kwargs = {'password': {'write_only': True}}
