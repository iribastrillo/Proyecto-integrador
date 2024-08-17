from django.contrib import admin
from .models import (
    AlumnoCurso,
    Carrera,
    Curso,
    Previa,
    AlumnoCarrera,
    BloqueDeClase,
    Salon,
    Leccion,
    Grupo,
    Examen,
    AlumnoExamen,
    Dia,
    Pago,
    FaltaProfesor,
)


admin.site.register(AlumnoCurso)
admin.site.register(Carrera)
admin.site.register(Curso)
admin.site.register(Previa)
admin.site.register(AlumnoCarrera)
admin.site.register(BloqueDeClase)
admin.site.register(Salon)
admin.site.register(Leccion)
admin.site.register(Grupo)
admin.site.register(Examen)
admin.site.register(AlumnoExamen)
admin.site.register(Dia)
admin.site.register(Pago)
admin.site.register(FaltaProfesor)
