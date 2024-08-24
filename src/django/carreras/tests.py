from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import Profesor
from datetime import date


class CarrerasTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        teacher = Profesor.objects.create (
            user=user,
            nombre="test",
            apellido="test",
            dni=45003001,
            fecha_nacimiento=date(2000, 6, 10),
            direccion="Calle Test 1243",
            telefono="091909090",
            email="falso@falso.com",
            sexo="M"
        )
        teacher.save()
    def test_anonymous_user_cannot_reach_list(self) -> None:
        response = self.client.get (reverse("careers"))
        self.assertEquals(response.status_code, 302)
    def test_anonymous_user_cannot_get_create(self) -> None:
        response = self.client.get(reverse("create-career"))
        self.assertEquals(response.status_code, 302)
    def test_anonymous_user_cannot_post_create(self) -> None:
        response = self.client.post(reverse("create-career"))
        self.assertEquals(response.status_code, 302)
    def test_admin_success_on_creation (self) -> None:
        pass