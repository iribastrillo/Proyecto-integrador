from django.urls import path
from . import views

urlpatterns = [
    path('detalle/', views.profile, name='profile'),
    ]