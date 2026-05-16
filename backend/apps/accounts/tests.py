from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationEndpointTests(APITestCase):
    register_url = "/api/v1/auth/register/"
    login_url = "/api/v1/auth/login/"
    refresh_url = "/api/v1/auth/refresh/"
    profile_url = "/api/v1/auth/profile/"

    def setUp(self) -> None:
        self.user_password = "StrongPassword123"

        self.user = User.objects.create_user(
            email="existing@example.com",
            password=self.user_password,
            full_name="Existing User",
            role="developer",
        )

    def test_register_user_success(self) -> None:
        payload = {
            "email": "newuser@example.com",
            "full_name": "New User",
            "password": "StrongPassword123",
            "role": "developer",
        }

        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_register_user_with_short_password_fails(self) -> None:
        payload = {
            "email": "shortpass@example.com",
            "full_name": "Short Password",
            "password": "123",
            "role": "developer",
        }

        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email="shortpass@example.com").exists())

    def test_register_user_without_email_fails(self) -> None:
        payload = {
            "full_name": "No Email User",
            "password": "StrongPassword123",
            "role": "developer",
        }

        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success_returns_tokens(self) -> None:
        payload = {
            "email": "existing@example.com",
            "password": self.user_password,
        }

        response = self.client.post(self.login_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

    def test_login_with_wrong_password_fails(self) -> None:
        payload = {
            "email": "existing@example.com",
            "password": "WrongPassword123",
        }

        response = self.client.post(self.login_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_without_password_fails(self) -> None:
        payload = {
            "email": "existing@example.com",
        }

        response = self.client.post(self.login_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token_success(self) -> None:
        login_response = self.client.post(
            self.login_url,
            {
                "email": "existing@example.com",
                "password": self.user_password,
            },
            format="json",
        )

        refresh_token = login_response.data["refresh"]

        response = self.client.post(
            self.refresh_url,
            {"refresh": refresh_token},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_token_with_invalid_token_fails(self) -> None:
        response = self.client.post(
            self.refresh_url,
            {"refresh": "invalid-token"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_without_token_fails(self) -> None:
        response = self.client.post(self.refresh_url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_profile_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_get_profile_without_authentication_fails(self) -> None:
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_success(self) -> None:
        self.client.force_authenticate(user=self.user)

        payload = {
            "full_name": "Updated User",
            "role": "developer",
        }

        response = self.client.patch(self.profile_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, "Updated User")