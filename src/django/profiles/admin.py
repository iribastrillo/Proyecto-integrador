from django.contrib import admin

from .models import Alumno, Profesor


admin.site.register(Alumno)
admin.site.register(Profesor)