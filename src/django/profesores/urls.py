from django.urls import path
from . import views

urlpatterns = [
    path('', ProfesorListView.as_view(), name='professors'),
    path('ficha-del-profesor/nuevo', views.ProfesorCreateView.as_view(), name='create-professor'),
    path('<slug>/detalle', ProfesorDetailView.as_view(), name='detail-professor'),
    path('<slug>/editar', ProfesorUpdateView.as_view(), name='update-professor'),
    path('<slug>/eliminar', ProfesorDeleteView.as_view(), name='delete-professor'),
    path('<slug>/pagos', views.Pagos.as_view(), name='payments-professor'),
]


