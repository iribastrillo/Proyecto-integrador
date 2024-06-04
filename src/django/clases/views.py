from django.shortcuts import render
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from domain.models import BloqueDeClase,Grupo
from django.urls import reverse_lazy
from domain.models import Profesor
from .forms import CreateGroupForm, BloqueDeClaseForm
from django.http import HttpResponseRedirect


class CreateBloqueDeClase(LoginRequiredMixin, CreateView):
    model = BloqueDeClase
    form_class = BloqueDeClaseForm
    template_name = 'clases/clases_form.html'
    success_url = reverse_lazy('clases:home-class-blocks')


class ListBloqueDeClases (LoginRequiredMixin, ListView):
    model = BloqueDeClase
    template_name = 'clases/clases_list.html'
    context_object_name='lista_clases'


class DetailBloqueDeClase(LoginRequiredMixin, DetailView):
    model = BloqueDeClase
    template_name = 'clases/clases_list.html'


class DeleteBloqueDeClase(LoginRequiredMixin, DeleteView):
    model = BloqueDeClase
    template_name = 'clases/confirm_delete.html'
    success_url=reverse_lazy('clases:list-class-blocks')


class UpdateBloqueDeClase(LoginRequiredMixin, UpdateView):
    model=BloqueDeClase
    fields = ['curso', 'alumnos_cursos', 'cupo', 'profesores', 'dia', 'duracion', 'hora_inicio', 'hora_fin', 'salon']
    template_name = 'clases/confirm_delete.html'
    success_url=reverse_lazy('clases:list-class-blocks')


def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        print(request.POST)
        if form.is_valid():
            curso = form.cleaned_data["curso"]
            alumnos = form.cleaned_data["alumnos"]
            profesores = form.cleaned_data["profesores"]
            cupo = form.cleaned_data["cupo"]
            groupo = Grupo(curso=curso, cupo=cupo)
            groupo.save()
            groupo.alumnos.set(alumnos)
            groupo.profesores.set(profesores)
            return HttpResponseRedirect(reverse_lazy('clases:list-class-groups'))
        else:
            print(form.errors)
    else:
        form = CreateGroupForm()
    return render(request, 'clases/clases_leccion_form.html', {'form': form})


def list_groups(request):
    grupos = Grupo.objects.all()
    return render(request, 'clases/grupo_list.html', {'lista_grupos': grupos})


def load_professors(request):
    curso_id = request.GET.get('curso')
    profesores = Profesor.objects.filter(cursos__id=curso_id)
    return render(request, 'clases/profesores_options.html', {'profesores': profesores})