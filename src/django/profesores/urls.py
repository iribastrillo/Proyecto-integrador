from django.urls import path
from .views import (
               ProfesorCreateView,
               ProfesorListView,
               ProfesorDetailView,
               ProfesorUpdateView,
               ProfesorDeleteView,
                )
app_name = 'profesores'  # Define the namespace

urlpatterns = [
    path('', ProfesorListView.as_view(), name='home-professor'),
    path('crear-profesor/', ProfesorCreateView.as_view(), name='create-professor'),
    path('listar-profesores/', ProfesorListView.as_view(), name='list-professors'),
    path('detalle-profesor/<int:pk>', ProfesorDetailView.as_view(), name='detail-professor'),
    path('editar-profesor/<int:pk>', ProfesorUpdateView.as_view(), name='update-professor'),
    path('eliminar-profesor/<int:pk>', ProfesorDeleteView.as_view(), name='delete-professor'),
]


