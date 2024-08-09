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
    # path("<slug>/falta_profesor", views.FaltaProfesorCreateView.as_view(), name="missing-professor"),
    path("<slug>/falta_profesor", views.falta_profesor, name="missing-professor"),
    path('<pk>/cargar-profesores/', views.load_professors, name='load-profesors'),

 ]
