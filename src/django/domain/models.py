from django.db import models
import datetime

class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=8)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    fecha_baja = models.DateField(null=True, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)
    activo=models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre + ' ' + self.apellido

# Create your models here.
class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    duracion_meses = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_baja = models.DateField(null=True, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='cursos', null=True, blank=True)
    activo=models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class Previas(models.Model):
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='curso')
    previa=models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='previa')

class Carrera(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    duracion_meses = models.IntegerField()
    fecha_baja = models.DateField()
    fecha_alta = models.DateField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='carreras', null=True, blank=True)
    cursos = models.ManyToManyField(Curso)
    activo=models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class Alumno(Persona):
    def __str__(self):
        return 'Alumno: '+self.nombre + ' ' + self.apellido

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

class Profesor(Persona):
    cursos = models.ManyToManyField(Curso)
    def __str__(self):
        return 'Profesor: '+self.nombre + ' ' + self.apellido


class Salon(models.Model):
    nombre=models.CharField(max_length=50)
    capacidad=models.IntegerField()
    activo=models.BooleanField(default=True)
    capacidad=models.IntegerField()
    def __str__(self):
        return self.nombre

class BloqueDeClase(models.Model):
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE)
    alumnos_cursos=models.ManyToManyField(AlumnoCurso) #validar que el alumno este inscripto en el curso, y que la cantidad sea menor o igual al cupo de la clase
    cupo=models.IntegerField() # Este cupo no debe ser mayor a la cantidad de personas que acepte el salon
    profesores=models.ManyToManyField(Profesor) #validar que el profesor este asignado al curso
    dia=models.CharField(max_length=500, choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miercoles', 'Miercoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sabado', 'Sabado'), ('Domingo', 'Domingos')])
    duracion=models.IntegerField()
    hora_inicio=models.TimeField()
    hora_fin=models.TimeField()
    salon=models.ForeignKey(Salon, on_delete=models.CASCADE)
    def __str__(self):
        return "Bloque de clase de " + self.curso.nombre + " el " + self.dia + " de " + str(self.hora_inicio) + " a " + str(self.hora_fin) + " en el salon " + self.salon.nombre


class Asistencia(models.Model):
    alumnos=models.ManyToManyField(Alumno)
    profesores=models.ManyToManyField(Profesor)
    bloque=models.ForeignKey(BloqueDeClase, on_delete=models.CASCADE)
    fecha=models.DateTimeField()
    temario=models.TextField()
    def __str__(self):
        return self.alumno.nombre