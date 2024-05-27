from django.db import models
from django.contrib.auth.models import User

from utils.validators import EmailValidator


class Persona(models.Model):
    user = models.ForeignKey (User, on_delete=models.CASCADE)
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

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre + ' ' + self.apellido
    
class Alumno(Persona):
    def __str__(self):
        return 'Alumno: '+self.nombre + ' ' + self.apellido
    
class Profesor(Persona):
    cursos = models.ManyToManyField('domain.Curso')
    def __str__(self):
        return 'Profesor: '+self.nombre + ' ' + self.apellido 

    def save(self, *args, **kwargs):
        user = User.objects.create_user(username=self.apellido, password=self.dni)
        user.save()
        self.user = user
        super().save(*args, **kwargs)