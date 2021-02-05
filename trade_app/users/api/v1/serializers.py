from rest_framework import serializers
from rest_framework_simplejwt.state import User

from trades.models import Inventory


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }
