from django.db import models
from django.urls import reverse

from profiles.models import Alumno, Profesor


class Dia(models.Model):
    WEEKDAYS=[
      ('LUN', 'Lunes'),
      ('MAR', 'Martes'),
      ('MIE', 'Miercoles'),
      ('JUE', 'Jueves'),
      ('VIE', 'Viernes'),
      ('SAB', 'Sábado'),
      ('DOM', 'Domingos')
      ]
    name = models.CharField(max_length=3, choices=WEEKDAYS)


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
    def __str__(self):
        return self.nombre
    def get_absolute_url(self):
        return reverse("courses")


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
    def __str__(self):
        return self.nombre
    def get_absolute_url(self):
        return reverse("careers")


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
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE)
    alumnos=models.ManyToManyField(Alumno, blank=True, null=True) #validar que el alumno este inscripto en el curso, y que la cantidad sea menor o igual al cupo de la clase
    cupo=models.IntegerField() # Este cupo no debe ser mayor a la cantidad de personas que acepte el salon
    profesores=models.ManyToManyField(Profesor) #validar que el profesor este asignado al curso
    dia=models.CharField(max_length=500, choices=WEEKDAYS)
    hora_inicio=models.TimeField()
    hora_fin=models.TimeField()
    salon=models.ForeignKey(Salon, on_delete=models.CASCADE)
    grupo=models.ForeignKey(Grupo, on_delete=models.CASCADE)

    def __str__(self):
        return "BLOQUE: " + self.dia.name + self.hora_inicio + " | " + self.salon.nombre


class Leccion(models.Model):
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE)
    alumnos=models.ManyToManyField(Alumno)
    profesores=models.ManyToManyField(Profesor)
    bloque=models.ForeignKey(BloqueDeClase, on_delete=models.CASCADE)
    fecha=models.DateTimeField()
    descripcion=models.TextField()