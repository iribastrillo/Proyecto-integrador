from django.shortcuts import render

from domain.models import (Salon)
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy
from domain.models import (Salon)
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class SalonesCreateView(LoginRequiredMixin,CreateView):
    model=Salon
    fields = ['nombre', 'capacidad','descripcion']
    template_name = 'salones/salones_form.html'

    success_url=reverse_lazy('salones:classrooms')

class SalonesListView(LoginRequiredMixin,ListView):
    model=Salon
    context_object_name='lista_salones'
    template_name = 'salones/salones_list.html'

class SalonesDetailView(LoginRequiredMixin,DetailView):
    model=Salon
    template_name = 'salones/salones_detail.html'

class SalonesUpdateView(LoginRequiredMixin,UpdateView):
    model=Salon
    fields = '__all__'
    template_name = 'salones/salones_form.html'
    success_url=reverse_lazy('salones:list-classrooms')

class SalonesDeleteView(LoginRequiredMixin,DeleteView):
    model=Salon
    template_name = 'salones/salones_confirm_delete.html'
    success_url=reverse_lazy('salones:list-classrooms')
