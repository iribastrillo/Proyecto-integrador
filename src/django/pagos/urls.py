from django.urls import path
from . import views

app_name = 'pagos'


urlpatterns = [
    # ... tus otras URLs
    path('agregar-pago/<slug>/', views.CreartePago.as_view(), name='add-payment'),
]