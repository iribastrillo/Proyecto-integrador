from django.urls import path
from .views import (
               SalonesCreateView,
               SalonesListView,
               SalonesDetailView,
               SalonesUpdateView,
               SalonesDeleteView,
                )


app_name = 'salones'

urlpatterns = [
    path('', SalonesListView.as_view(), name='classrooms'),
    path('crear-salon/', SalonesCreateView.as_view(), name='create-classroom'),
    path('detalle-salon/<int:pk>', SalonesDetailView.as_view(), name='detail-classroom'),
    path('editar-salon/<int:pk>', SalonesUpdateView.as_view(), name='update-classroom'),
    path('eliminar-salon/<int:pk>', SalonesDeleteView.as_view(), name='delete-classroom'),
]