# apps/accounts/serializers.py
from typing import Any, Dict
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: Any) -> Token:
        token: Token = super().get_token(user)
        token['email'] = user.email
        token['role'] = getattr(user, 'role', 'developer')
        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data: Dict[str, Any] = super().validate(attrs)
        data.update({
            'user': {
                'id': self.user.id,
                'email': self.user.email,
                'full_name': getattr(self.user, 'full_name', ''),
                'role': getattr(self.user, 'role', 'developer'),
            }
        })
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password: serializers.CharField = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'role')

    def create(self, validated_data: Dict[str, Any]) -> Any:
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'role', 'avatar', 'created_at')
        read_only_fields = ('id', 'email', 'created_at')