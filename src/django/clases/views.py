from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from domain.models import BloqueDeClase,Grupo
from django.urls import reverse_lazy
from domain.models import Profesor
from django.http import HttpResponseRedirect

from .forms import CreateGroupForm, BloqueDeClaseForm


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


@login_required
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        print(request.POST)
        if form.is_valid():
            curso = form.cleaned_data["curso"]
            profesores = form.cleaned_data["profesores"]
            cupo = form.cleaned_data["cupo"]
            groupo = Grupo(curso=curso, cupo=cupo)
            groupo.save()

            # Use .set() for many-to-many fields
            groupo.profesores.set(profesores)
            return HttpResponseRedirect(reverse_lazy('clases:list-class-groups'))
        else:
            print(form.errors)
    else:
        form = CreateGroupForm()
    return render(request, 'clases/create_grupo_form.html', {'form': form})


@login_required
def update_group(request, pk):
    group = get_object_or_404(Grupo, id=pk)
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group.curso = form.cleaned_data["curso"]
            group.cupo = form.cleaned_data["cupo"]
            group.save()
            group.alumnos.set(form.cleaned_data["alumnos"])
            group.profesores.set(form.cleaned_data["profesores"])
            return HttpResponseRedirect(reverse_lazy('clases:list-class-groups'))
    else:
        form_data = {
            'curso': group.curso,
            'alumnos': group.alumnos.all(),
            'profesores': group.profesores.all(),
            'cupo': group.cupo,
        }
        form = CreateGroupForm(initial=form_data)
    return render(request, 'clases/clases_leccion_form.html', {'form': form})

@login_required
def delete_group(request, pk):
    grupo = get_object_or_404(Grupo, id=pk)
    print(grupo.__dict__)

    if request.method == 'POST':
        grupo.delete()
        return redirect(reverse_lazy('clases:list-class-groups'))
    return render(request, 'clases/grupo_confirm_delete.html', {'grupo': grupo})

def list_groups(request):
    grupos = Grupo.objects.all()
    return render(request, 'clases/grupo_list.html', {'lista_grupos': grupos})

def load_professors(request):
    curso_id = request.GET.get('curso')
    profesores = Profesor.objects.filter(cursos__id=curso_id)
    return render(request, 'clases/profesores_options.html', {'profesores': profesores})