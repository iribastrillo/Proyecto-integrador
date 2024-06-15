from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError
from utils.validators import EmailValidator
from django.urls import reverse

from core.domain.services import generate_unique_code


class Persona(models.Model):
    slug = models.SlugField(max_length=8, unique=True, null=True, blank=True)
    user = models.ForeignKey (User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=8)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(validators=[EmailValidator()])
    fecha_baja = models.DateField(null=True, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)
    activo=models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        try:
            user = User.objects.get(username=self.slug)
        except User.DoesNotExist as e:
            while True:
                new_code = generate_unique_code()
                print(new_code)
                try:
                    user = User.objects.create (username=new_code, password=self.dni)
                    break
                except IntegrityError as e:
                    pass
            self.slug = new_code
            self.user = user
        user.first_name = self.nombre
        user.last_name = self.apellido
        user.email = self.email
        user.save()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

class Alumno(Persona):
    def __str__(self):
        return f'Alumno: {self.apellido}, {self.nombre}'


class Profesor(Persona):
    cursos = models.ManyToManyField('domain.Curso')
    def __str__(self):
        return f'Profesor: {self.apellido}, {self.nombre}'