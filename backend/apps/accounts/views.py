# apps/accounts/views.py
from typing import Any

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.translation import gettext_lazy as _

message = _("This is a message in the accounts/views app.")

from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        summary="User Login (Obtain JWT Token)",
        description="Takes user credentials (email and password) and returns access and refresh JWT tokens along with basic user info.",
        responses={200: CustomTokenObtainPairSerializer},
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Register a new user",
        description="Creates a new user account in the system. Password will be securely hashed.",
        responses={201: RegisterSerializer, 400: None},
    )
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Get current user profile",
        description="Returns detailed profile information of the currently authenticated user. **Requires JWT Token**.",
        responses={200: UserProfileSerializer, 401: None},
    ),
    put=extend_schema(
        summary="Full update of user profile",
        description="Updates full profile details. **Requires JWT Token**.",
        responses={200: UserProfileSerializer, 401: None, 400: None},
    ),
    patch=extend_schema(
        summary="Partial update of user profile",
        description="Updates specific profile fields (e.g., avatar or full_name). **Requires JWT Token**.",
        responses={200: UserProfileSerializer, 401: None, 400: None},
    ),
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self) -> Any:
        return self.request.user
