from django.urls import path
from . import views

app_name = "clases"

urlpatterns = [
    path('', views.ListBloqueDeClases.as_view(), name='home-class-blocks'),
    path('bloques/crear/<int:pk>/', views.CreateBloqueDeClase.as_view(), name='create-class-block'),
    path('bloques/', views.ListBloqueDeClases.as_view(), name='list-class-blocks'),
    path('bloques/<int:pk>/detalle', views.DetailBloqueDeClase.as_view(), name='detail-class-block'),
    path('bloques/<int:pk>/editar', views.BloqueClaseUpdateView.as_view(), name='update-class-block'),
    path('bloques/<int:pk>/eliminar', views.DeleteBloqueDeClase.as_view(), name='delete-class-block'),
    path('grupos/',views.list_groups, name='list-groups'),
    path('grupos/crear',  views.CreateGrupo.as_view(), name='create-group'),
    # path('grupos/crear', views.create_group, name='create-group'),
    # path('grupos/<int:pk>/editar', views.update_group, name='update-group'),
    path('grupos/<int:pk>/editar', views.UpdateGrupo.as_view(), name='update-group'),
    path('grupos/<int:pk>/eliminar', views.delete_group, name='delete-group'),
    path('grupos/<int:pk>/detalle', views.GrupoDetailView.as_view(), name='detail-group'),
    path('grupos/cargar-profesores/', views.load_professors, name='load-profesors'),
    path('grupos/<int:pk>/cargar-profesores/', views.load_professors, name='load-profesors'),
    path('grupos/<int:pk>/cargar-horas-disponibles/', views.load_available_hours, name='load-hours'),
    path('grupos/cargar-grupo/', views.load_group, name='load-group'),
]
