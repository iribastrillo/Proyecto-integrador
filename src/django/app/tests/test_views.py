from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class LoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()

    def setUp(self) -> None:
        self.client = Client()

    def test_template_is_correct(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "registration/login.html")

    def test_user_logs_in(self) -> None:
        loggedin = self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("home"))
        self.assertTrue(loggedin)
        self.assertEquals(response.status_code, 200)

    def test_user_fails_log_in(self) -> None:
        loggedin = self.client.login(username="testuser", password="156")
        response = self.client.get(reverse("home"))
        self.assertFalse(loggedin)
        self.assertEquals(response.status_code, 302)


class TestHome(TestCase):
    def test_unauthenticated_user_cant_reach_home(self) -> None:
        response = self.client.get(reverse("home"))
        self.assertEquals(response.status_code, 302)
