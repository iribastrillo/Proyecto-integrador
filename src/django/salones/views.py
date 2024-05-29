from django.shortcuts import render

from domain.models import (Salones)
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.models import Salon
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class SalonesCreateView(LoginRequiredMixin,CreateView):
    model=Salon
    fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'direccion', 'telefono','email','cursos']
    success_url=reverse_lazy('salones:home-classroom')

class SalonesListView(LoginRequiredMixin,ListView):
    model=Salon
    # template_name = 'salones/listar_salones.html'
    context_object_name='lista_salones'

class SalonesDetailView(LoginRequiredMixin,DetailView):
    model=Salon
    # template_name = 'domain/salon_detail.html'

class SalonesUpdateView(LoginRequiredMixin,UpdateView):
    model=Salon
    fields = '__all__'
    # template_name = 'domain/salon_update.html'
    success_url=reverse_lazy('salones:list-classrooms')

class SalonesDeleteView(LoginRequiredMixin,DeleteView):
    model=Salon
    # template_name = 'domain/salon_delete.html'
    success_url=reverse_lazy('salones:list-classrooms')
