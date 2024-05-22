from django.contrib import admin

# Register your models here.

from .models import Alumno, AlumnoCurso, Carrera, Curso, Previas, Profesor, AlumnoCarrera, BloqueDeClase,Salon,Asistencia

admin.site.register(Alumno)
admin.site.register(AlumnoCurso)
admin.site.register(Carrera)
admin.site.register(Curso)
admin.site.register(Previas)
admin.site.register(AlumnoCarrera)
admin.site.register(BloqueDeClase)
admin.site.register(Salon)
admin.site.register(Asistencia)
admin.site.register(Profesor)


