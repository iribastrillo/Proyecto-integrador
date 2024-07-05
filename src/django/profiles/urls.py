from django.urls import path
from . import views
from estudiantes import views as estudiantes
from profesores import views as profesores

app_name='profiles'

urlpatterns = [
    path('', views.profile, name=''),
    path('editar', views.UpdateProfile.as_view(), name='update'),
    path('estudiante/<slug>/editar', estudiantes.AlumnoUpdateView.as_view(), name='update-student'),
    path('profesor/<slug>/editar', profesores.ProfesorUpdateView.as_view(), name='update-professor'),
    path('usuarios', views.ProfessorsAndStudents.as_view(), name='users'),
]