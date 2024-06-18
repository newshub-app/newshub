from django.test import TestCase
from django.urls import reverse

EXAMPLE_USER = {
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "password": "SecureTestPassword123!",
    "email": "testuser@example.com",
}


class AuthenticationTestCase(TestCase):
    def test_login(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, "Login", status_code=200)

    def test_register(self):
        response = self.client.post(reverse("register"), data=EXAMPLE_USER)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
