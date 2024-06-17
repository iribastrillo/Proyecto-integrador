from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('usuarios', views.ProfessorsAndStudents.as_view(), name='users'),
    ]