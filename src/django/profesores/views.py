from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from domain.models import Profesor

from core.domain.services import calculate_payment


class ProfesorCreateView(LoginRequiredMixin,CreateView):
    model=Profesor
    fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'direccion', 'telefono','email','cursos']
    success_url=reverse_lazy('professors')

class ProfesorListView(LoginRequiredMixin,ListView):
    model=Profesor
    # template_name = 'profesores/listar_profesores.html'
    context_object_name='lista_profesores'

class ProfesorDetailView(LoginRequiredMixin,DetailView):
    model=Profesor
    # template_name = 'domain/profesor_detail.html'

class ProfesorUpdateView(LoginRequiredMixin,UpdateView):
    model=Profesor
    fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'direccion', 'telefono', 'email', 'cursos']
    def get_success_url(self):
        return reverse_lazy("detail-professor", kwargs={"slug": self.object.user.username})

class ProfesorDeleteView(LoginRequiredMixin,DeleteView):
    model=Profesor
    success_url=reverse_lazy('profesores:list-professors')

class Pagos (View):
    template_name = 'profesores/payments.html'
    
    def get (self, request, *args, **kwargs):
        professor = Profesor.objects.get (slug = kwargs['slug'])
        groups = professor.grupo_set.all()
        context = {
            'profesor': professor,
            'monthly_payment' : calculate_payment(groups),
            'groups': groups
        }
        return render (request, self.template_name, context)