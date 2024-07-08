from django.urls import path
from . import views

app_name = 'pagos'


urlpatterns = [
    path('agregar-pago/<slug>/', views.CreartePago.as_view(), name='add-payment'),
    path('modificar-pago/<pk>/', views.UpdatePago.as_view(), name='update-payment'),
    path('detalle-pago/<pago_id>/', views.DetailPago.as_view(), name='detail-payment'),
    path('listar-pagos/<slug>/', views.ListPagos.as_view(), name='payments'),
    path('eliminar-pago/<pk>/', views.DeletePago.as_view(), name='delete-payment'),
]