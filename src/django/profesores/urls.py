from django.urls import path
from .views import (
               ProfesorCreateView,
               ProfesorListView,
               ProfesorDetailView,
               ProfesorUpdateView,
               ProfesorDeleteView,
                )

urlpatterns = [
    path('', ProfesorListView.as_view(), name='professors'),
    path('crear-profesor/', ProfesorCreateView.as_view(), name='create-professor'),
    path('<slug>/detalle', ProfesorDetailView.as_view(), name='detail-professor'),
    path('<slug>/editar', ProfesorUpdateView.as_view(), name='update-professor'),
    path('<slug>/eliminar', ProfesorDeleteView.as_view(), name='delete-professor'),
]


