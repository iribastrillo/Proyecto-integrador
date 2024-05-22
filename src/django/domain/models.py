from django.db import models
from django.http.response import HttpResponse


def home_view(request):
    return HttpResponse("Domain Home Page")

# Create your models here.
class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    duracion_meses = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='cursos', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Carrera(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    duracion_meses = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='carreras', null=True, blank=True)
    cursos = models.ManyToManyField(Curso)
    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=8)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    cursos = models.ManyToManyField(Curso)
    def __str__(self):
        return 'Alumno: '+self.nombre + ' ' + self.apellido

class Profesor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=8)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    cursos = models.ManyToManyField(Curso)
    def __str__(self):
        return 'Profesor: '+self.nombre + ' ' + self.apellido