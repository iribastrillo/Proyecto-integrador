from django.urls import path
from .views import (
               HomeView,
               GraciasView,
               ContactFormView,
               ProfesorCreateView,
               ProfesorListView,
               ProfesorDetailView,
               ProfesorUpdateView,
               ProfesorDeleteView,
                )

app_name = 'domain'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('gracias/', GraciasView.as_view(), name='gracias'),
    path('contacto/', ContactFormView.as_view(), name='contacto'),
    path('create_profesor/', ProfesorCreateView.as_view(), name='crear_profesor'),
    path('list_profesor/', ProfesorListView.as_view(), name='listar_profesor'),
    path('detail_profesor/<int:pk>', ProfesorDetailView.as_view(), name='detalle_profesor'),
    path('update_profesor/<int:pk>', ProfesorUpdateView.as_view(), name='editar_profesor'),
    path('delete_profesor/<int:pk>', ProfesorDeleteView.as_view(), name='eliminar_profesor'),
    ]