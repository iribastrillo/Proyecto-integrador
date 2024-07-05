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
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class SalonesCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model=Salon
    fields = ['nombre', 'capacidad','descripcion']
    template_name = 'salones/salones_form.html'
    success_url=reverse_lazy('salones:classrooms')
    success_message = "Se creó el salón con éxito"

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field in form.errors:
            for error in form.errors[field]:
                messages.add_message(self.request, messages.ERROR, error)
        return response


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
    success_url=reverse_lazy('salones:classrooms')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if 'nombre' in form.errors:
            print(f"Nombre form errors: {form.errors['nombre']}")
            for error in form.errors['nombre']:
                messages.add_message(self.request, messages.ERROR, error)
        if 'capacidad' in form.errors:
            print(f"Capacidad form errors: {form.errors['capacidad']}")
            for error in form.errors['capacidad']:
                messages.add_message(self.request, messages.ERROR, error)
        return response


class SalonesDeleteView(LoginRequiredMixin,DeleteView):
    model=Salon
    template_name = 'salones/salones_confirm_delete.html'
    success_url=reverse_lazy('salones:classrooms')
    success_message = "El salon se eliminó con éxito"
