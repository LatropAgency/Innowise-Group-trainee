from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.state import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }
