from django.urls import path
from .views import (
               HomeView,
               GraciasView,
               ContactFormView
                )

app_name = 'domain'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('gracias/', GraciasView.as_view(), name='gracias'),
    path('contacto/', ContactFormView.as_view(), name='contacto'),

    ]