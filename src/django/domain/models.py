from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

from profiles.models import Alumno, Profesor


class Dia(models.Model):
    WEEKDAYS=[
      ('LUN', 'Lunes'),
      ('MAR', 'Martes'),
      ('MIE', 'Miércoles'),
      ('JUE', 'Jueves'),
      ('VIE', 'Viernes'),
      ('SAB', 'Sábado'),
      ('DOM', 'Domingos')
      ]
    name = models.CharField(max_length=3, choices=WEEKDAYS)

    def __str__(self) -> str:
        return self.name


class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    duracion_meses = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_baja = models.DateField(null=True, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='cursos', null=True, blank=True)
    activo=models.BooleanField(default=True)
    payout_ratio = models.DecimalField (max_digits=3, decimal_places=2, validators=[
        MaxValueValidator(1, "El valor debe estar entre 1 y 0."),
        MinValueValidator(0, "El valor debe estar entre 1 y 0.")
        ], default=0.5)
    slug = models.SlugField(max_length=50)
    
    def __str__(self):
        return self.nombre
    def get_absolute_url(self):
        return reverse("courses")
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Previa(models.Model):
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='curso')
    previa=models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='previa')


class Carrera(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    duracion_meses = models.IntegerField()
    fecha_baja = models.DateField(null=True, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='carreras', null=True, blank=True)
    cursos = models.ManyToManyField(Curso)
    activo=models.BooleanField(default=True)
    slug = models.SlugField(max_length=50)
    def __str__(self):
        return self.nombre
    def get_absolute_url(self):
        return reverse("careers")
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class AlumnoCurso(models.Model):
    alumno=models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion=models.DateTimeField(auto_now_add=True)
    fecha_finalizado=models.DateTimeField(null=True, blank=True)
    aprobado=models.BooleanField(default=False)
    def __str__(self):
        return 'Inscripcion: '+self.alumno.nombre + ' ' + self.curso.nombre


class AlumnoCarrera(models.Model):
    alumno=models.ForeignKey(Alumno, on_delete=models.CASCADE)
    carrera=models.ForeignKey(Carrera, on_delete=models.CASCADE)
    fecha_inscripcion=models.DateTimeField(auto_now_add=True)
    fecha_finalizado=models.DateTimeField(null=True, blank=True)
    aprobado=models.BooleanField(default=False)
    def __str__(self):
        return 'Inscripcion: '+self.alumno.nombre + ' ' + self.curso.nombre


class Salon(models.Model):
    nombre=models.CharField(max_length=50)
    capacidad=models.IntegerField(null=True, blank=True)
    activo=models.BooleanField(default=True)
    descripcion=models.TextField(null=True, blank=True,default=None)
    def __str__(self):
        return self.nombre


class Grupo (models.Model):
    identificador = models.CharField(max_length=1)
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE)
    alumnos=models.ManyToManyField(Alumno, blank=True) #validar que el alumno este inscripto en el curso, y que la cantidad sea menor o igual al cupo de la clase
    cupo=models.IntegerField()
    profesores=models.ManyToManyField(Profesor) #validar que el profesor este asignado al curso

    def __str__(self) -> str:
        return f"Grupo {self.pk} | {self.curso.nombre}"


class BloqueDeClase(models.Model):
    dia=models.ManyToManyField(Dia)
    hora_inicio=models.TimeField()
    hora_fin=models.TimeField()
    salon=models.ForeignKey(Salon, on_delete=models.CASCADE)
    grupo=models.ForeignKey(Grupo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.hora_inicio} - {self.hora_fin}: {self.grupo}"


class Leccion(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    alumnos=models.ManyToManyField(Alumno, blank=True)
    profesores=models.ManyToManyField(Profesor, blank=True)
    bloque=models.ForeignKey(BloqueDeClase, on_delete=models.CASCADE)
    fecha=models.DateTimeField()
    descripcion=models.TextField(max_length=250, blank=True, null=True)
    
    def __str__(self):
        return f"Lección: {self.grupo} {self.bloque.hora_inicio} - {self.bloque.hora_fin}"