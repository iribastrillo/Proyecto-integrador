from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from utils.validators import EmailValidator
from django.urls import reverse
from django.utils import timezone

from datetime import date

from core.domain.services import generate_unique_code


class Persona(models.Model):
    slug = models.SlugField(max_length=8, unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=8)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(validators=[EmailValidator()], null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)
    sexo = models.CharField(
        max_length=1, choices=[("M", "Masculino"), ("F", "Femenino")]
    )

    def save(self, *args, **kwargs):
        try:
            user = User.objects.get(username=self.slug)
        except User.DoesNotExist as e:
            while True:
                new_code = generate_unique_code()
                print(new_code)
                try:
                    user = User.objects.create(
                        username=new_code, password=make_password(self.dni)
                    )
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

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)
        
    @property
    def is_active (self):
        return self.user.is_active

    class Meta:
        abstract = True


class Alumno(Persona):
    emergency_contact = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Alumno: {self.apellido}, {self.nombre}"

    @property
    def is_up_to_date_with_payments(self):
        enrolments = self.alumnocurso_set.all()
        payments = self.pago_set.filter(fecha__month=date.today().month)
        up_to_date = True
        for enrolment in enrolments:
            try:
                up_to_date = up_to_date and payments.get(curso=enrolment.curso).exists()
            except AttributeError as e:
                pass
        return up_to_date

    @property
    def age(self):
        if self.fecha_nacimiento:
            today = timezone.now().date()
            age = int(
                today.year
                - (self.fecha_nacimiento.year)
                - (
                    (today.month, today.day)
                    < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
                )
            )
            return age
        
    @property
    def active_enrolents(self):
        return self.alumnocurso_set.filter(fecha_baja=None).count()
    
    def get_absolute_url(self):
        return reverse("estudiantes:detail-student", kwargs={"slug": self.slug})


class Profesor(Persona):
    cursos = models.ManyToManyField("domain.Curso")

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    def get_absolute_url(self):
        return reverse("detail-professor", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = "Profesores"
        permissions = [("is_professor", "Es profesor")]
