
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from accounts.models import User


class AuthenticationTests(APITestCase):

    def test_user_registration(self):
        url = reverse("register")

        response = self.client.post(url, {
            "name": "Amit Kumar",
            "email": "amitnew@example.com",
            "password": "StrongPassword@123"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(email="amitnew@example.com").exists()
        )

    def test_user_login(self):
        User.objects.create_user(
            email="login@example.com",
            name="Login User",
            password="TestPassword@123"
        )

        url = reverse("login")

        response = self.client.post(url, {
            "email": "login@example.com",
            "password": "TestPassword@123"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_wrong_password(self):
        User.objects.create_user(
            email="wrongpass@example.com",
            name="Wrong Password User",
            password="TestPassword@123"
        )

        url = reverse("login")

        response = self.client.post(url, {
            "email": "wrongpass@example.com",
            "password": "WrongPassword@123"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_duplicate_email_registration(self):
        User.objects.create_user(
            email="duplicate@example.com",
            name="Existing User",
            password="TestPassword@123"
        )

        url = reverse("register")

        response = self.client.post(url, {
            "name": "New User",
            "email": "duplicate@example.com",
            "password": "StrongPassword@123"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
