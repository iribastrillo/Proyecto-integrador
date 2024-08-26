from django.urls import path
from . import views


app_name = "estudiantes"

urlpatterns = [
    path("", views.AlumnoListView.as_view(), name="students"),
    path("dashboard/", views.Dashboard.as_view(), name="dashboard"),
    path(
        "ficha-del-estudiante/nuevo",
        views.AlumnoCreateView.as_view(),
        name="create-student",
    ),
    path(
        "inscripcion/<slug>/nuevo",
        views.InscripcionNueva.as_view(),
        name="enrolment-student",
    ),
    path(
        "inscripcion/<slug>/bajar",
        views.BajaEstudiante.as_view(),
        name="resign-student",
    ),
    path("<slug>/detalle", views.AlumnoDetailView.as_view(), name="detail-student"),
    path("<slug>/editar", views.AlumnoUpdateView.as_view(), name="update-student"),
    path("<slug>/eliminar", views.AlumnoDeleteView.as_view(), name="delete-student"),
    path(
        "<slug>/inhabilitar",
        views.InhabilitarAlumno.as_view(),
        name="disable-student",
    ),
    path(
        "<slug>/habilitar",
        views.HabilitarAlumno.as_view(),
        name="enable-student",
    ),
    path(
        "grupos/",
        views.Groups.as_view(),
        name="groups",
    ),
    path(
        "cambiar/<slug>/grupo/<id>/", views.CambioDeGrupo.as_view(), name="change-group"
    ),
]
