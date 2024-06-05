from django.urls import path
from .views import (
               CreateBloqueDeClase,
               ListBloqueDeClases,
                DetailBloqueDeClase,
                UpdateBloqueDeClase,
                DeleteBloqueDeClase,
                create_group,
                load_professors,
                list_groups,
                update_group,
                delete_group,
                detail_group
                )


app_name = 'clases'

urlpatterns = [
    path('', ListBloqueDeClases.as_view(), name='home-class-blocks'),
    path('bloques/crear', CreateBloqueDeClase.as_view(), name='create-class-block'),
    path('bloques/', ListBloqueDeClases.as_view(), name='list-class-blocks'),
    path('bloques/<int:pk>/detalle', DetailBloqueDeClase.as_view(), name='detail-class-block'),
    path('bloques/<int:pk>/editar', UpdateBloqueDeClase.as_view(), name='update-class-block'),
    path('bloques/<int:pk>/eliminar', DeleteBloqueDeClase.as_view(), name='delete-class-block'),
    path('grupos/',list_groups, name='list-groups'),
    path('grupos/crear', create_group, name='create-group'),
    path('grupos/<int:pk>/editar', update_group, name='update-group'),
    path('grupos/<int:pk>/eliminar', delete_group, name='delete-group'),
    path('grupos/<int:pk>/detalle', detail_group, name='detail-group'),
    path('grupos/cargar-profesores/', load_professors, name='load-profesors')
]