from django.urls import path
from .views import AlumnoCreateView, AlumnoListView, AlumnoDetailView, AlumnoUpdateView, InscripcionNueva, BajaEstudiante, AlumnoDeleteView


app_name = 'estudiantes'

urlpatterns = [
    path('', AlumnoListView.as_view(), name='students'),
    path('ficha-del-estudiante/nuevo', AlumnoCreateView.as_view(), name='create-student'),
    path('inscripcion/<slug>/nuevo', InscripcionNueva.as_view(), name='enrolment-student'),
    path('inscripcion/<slug>/bajar', BajaEstudiante.as_view(), name='resign-student'),
    path('<slug>/detalle', AlumnoDetailView.as_view(), name='detail-student'),
    path('<slug>/editar', AlumnoUpdateView.as_view(), name='update-student'),
    path('<slug>/eliminar', AlumnoDeleteView.as_view(), name='delete-student'),
]



