# apps/accounts/tests.py
from typing import Any

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationTests(APITestCase):

    def setUp(self) -> None:
        self.register_url: str = reverse("auth_register")
        self.login_url: str = reverse("auth_login")

        self.user_data: dict[str, Any] = {
            "email": "testuser@kbtu.kz",
            "password": "StrongPassword123",
            "full_name": "John Doe",
            "role": "developer",
        }
        # Создаем пользователя заранее для тестов авторизации
        self.user: User = User.objects.create_user(
            email="existing@kbtu.kz",
            password="CorrectPassword123",
            full_name="Existing User",
            role="developer",
        )

    # ==========================================
    # TESTS: Registration Endpoint
    # ==========================================
    def test_registration_success(self) -> None:
        """1. Хороший кейс: Успешная регистрация с валидными данными."""
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertNotIn("password", response.data)  # Пароль не должен возвращаться

    def test_registration_failed_duplicate_email(self) -> None:
        """2. Плохой кейс: Ошибка при попытке зарегистрировать уже существующий email."""
        duplicate_data = self.user_data.copy()
        duplicate_data["email"] = "existing@kbtu.kz"  # Этот email уже занят в setUp

        response = self.client.post(self.register_url, duplicate_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_failed_short_password(self) -> None:
        """3. Плохой кейс: Ошибка валидации, если пароль меньше 8 символов."""
        weak_data = self.user_data.copy()
        weak_data["password"] = "123"

        response = self.client.post(self.register_url, weak_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    # ==========================================
    # TESTS: Login (JWT Token Obtain) Endpoint
    # ==========================================
    def test_login_success(self) -> None:
        """1. Хороший кейс: Получение токенов при правильных кредах."""
        login_data = {"email": "existing@kbtu.kz", "password": "CorrectPassword123"}
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["email"], "existing@kbtu.kz")

    def test_login_failed_wrong_password(self) -> None:
        """2. Плохой кейс: Ошибка 401 при неверном пароле."""
        wrong_password_data = {
            "email": "existing@kbtu.kz",
            "password": "WrongPassword!",
        }
        response = self.client.post(self.login_url, wrong_password_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_failed_invalid_email(self) -> None:
        """3. Плохой кейс: Ошибка 401, если пользователя с таким email нет в системе."""
        wrong_email_data = {
            "email": "fakeuser@kbtu.kz",
            "password": "CorrectPassword123",
        }
        response = self.client.post(self.login_url, wrong_email_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
