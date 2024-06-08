from django.urls import path
from .views import AlumnoCreateView, AlumnoListView, AlumnoDetailView, AlumnoUpdateView, InscripcionNueva, BajaEstudiante


app_name = 'estudiantes'

urlpatterns = [
    path('', AlumnoListView.as_view(), name='students'),
    path('ficha-del-estudiante/nuevo', AlumnoCreateView.as_view(), name='create-student'),
    path('inscripcion/<pk>/nuevo', InscripcionNueva.as_view(), name='enrolment-student'),
    path('inscripcion/<pk>/bajar', BajaEstudiante.as_view(), name='resign-student'),
    path('<int:pk>/detalle', AlumnoDetailView.as_view(), name='detail-student'),
    path('<int:pk>/editar', AlumnoUpdateView.as_view(), name='update-student'),
    path('<int:pk>/eliminar', AlumnoUpdateView.as_view(), name='delete-student'),
]



