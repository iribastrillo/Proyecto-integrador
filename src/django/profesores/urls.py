from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProfesorListView.as_view(), name="professors"),
    path(
        "ficha-del-profesor/nuevo",
        views.ProfesorCreateView.as_view(),
        name="create-professor",
    ),
    path("<slug>/detalle", views.ProfesorDetailView.as_view(), name="detail-professor"),
    path("<slug>/editar", views.ProfesorUpdateView.as_view(), name="update-professor"),
    path(
        "<slug>/eliminar", views.ProfesorDeleteView.as_view(), name="delete-professor"
    ),
    path("<slug>/pagos", views.Pagos.as_view(), name="payments-professor"),
    path("<slug>/reporte_clases", views.reporte_clases, name="report-professor-class"),
    path("<slug>/falta_profesor", views.falta_profesor_create, name="missing-professor"),
    path("<slug>/listar_faltas", views.list_faltas_profesor, name="list-missing-professor"),
    path("<pk>/modificar_falta", views.update_falta, name="update-falta"),
    path("<pk>/detail_falta", views.FaltaProfesorDetailView.as_view(), name="detail-falta"),
    path("<pk>/eliminar_falta", views.DeleteFaltaProfesor.as_view(), name="delete-falta"),
    path('<pk>/cargar-profesores/', views.load_professors, name='load-profesors'),

 ]
