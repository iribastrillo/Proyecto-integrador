from django.shortcuts import render
from domain.models import (Profesor)
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class ProfesorCreateView(LoginRequiredMixin,CreateView):
    model=Profesor
    fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'direccion', 'telefono','email','cursos']
    success_url=reverse_lazy('profesores:home-professor')

class ProfesorListView(LoginRequiredMixin,ListView):
    model=Profesor
    # template_name = 'profesores/listar_profesores.html'
    context_object_name='lista_profesores'

class ProfesorDetailView(LoginRequiredMixin,DetailView):
    model=Profesor
    # template_name = 'domain/profesor_detail.html'

class ProfesorUpdateView(LoginRequiredMixin,UpdateView):
    model=Profesor
    fields = '__all__'
    # template_name = 'domain/profesor_update.html'
    success_url=reverse_lazy('profesores:list-professors')

class ProfesorDeleteView(LoginRequiredMixin,DeleteView):
    model=Profesor
    # template_name = 'domain/profesor_delete.html'
    success_url=reverse_lazy('profesores:list-professors')
