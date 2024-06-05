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
                delete_group
                )


app_name = 'clases'

urlpatterns = [
    path('', ListBloqueDeClases.as_view(), name='home-class-blocks'),
    path('crear-clase/', CreateBloqueDeClase.as_view(), name='create-class-block'),
    path('listar-clases/', ListBloqueDeClases.as_view(), name='list-class-blocks'),
    path('detalle-clase/<int:pk>', DetailBloqueDeClase.as_view(), name='detail-class-block'),
    path('editar-clase/<int:pk>', UpdateBloqueDeClase.as_view(), name='update-class-block'),
    path('eliminar-clase/<int:pk>', DeleteBloqueDeClase.as_view(), name='delete-class-block'),
    path('eliminar-clase/<int:pk>', DeleteBloqueDeClase.as_view(), name='delete-class-block'),
    path('crear-grupo/', create_group, name='create-group'), ## esto funciona pero voy a probar model view
    path('eliminar-grupo/<int:pk>/', delete_group, name='delete-group'),
    # path('crear-groupo/', CreateGroupForm, name='create-group'),
    path('crear-grupo/cargar-profesores/', load_professors, name='load-profesors'),
      path('listar-grupos/',list_groups, name='list-class-groups'),
    path('editar-grupo/<int:pk>/', update_group, name='update-group'),
]
