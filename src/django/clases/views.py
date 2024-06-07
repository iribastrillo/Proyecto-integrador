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
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

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
    BloqueDeClaseFormSet = modelformset_factory(BloqueDeClase, form=BloqueDeClaseForm, extra=1)
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        formset = BloqueDeClaseFormSet(request.POST)

        print(request.POST)
        if form.is_valid() and formset.is_valid():
            curso = form.cleaned_data["curso"]
            profesores = form.cleaned_data["profesores"]
            cupo = form.cleaned_data["cupo"]
            groupo = Grupo(curso=curso, cupo=cupo)
            groupo.save()

            for bloque_form in formset:
                print(bloque_form)
                bloque = bloque_form.save(commit=False)
                bloque.grupo = groupo
                bloque.save()
                bloque_form.save_m2m()  # Save the ManyToManyField data
            # Use .set() for many-to-many fields
            groupo.profesores.set(profesores)
            return HttpResponseRedirect(reverse_lazy('clases:list-groups'))
        else:
            print(form.errors)
    else:
        form = CreateGroupForm()
        formset = BloqueDeClaseFormSet(queryset=BloqueDeClase.objects.none())

    return render(request, 'clases/create_grupo_form.html', {'form': form, 'formset': formset})


@login_required
def update_group(request, pk):
    group = get_object_or_404(Grupo, id=pk)
    BloqueDeClaseFormSet = modelformset_factory(BloqueDeClase, form=BloqueDeClaseForm, extra=0)

    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        formset = BloqueDeClaseFormSet(request.POST, queryset=BloqueDeClase.objects.filter(grupo=group))

        if form.is_valid() and formset.is_valid():
            group.curso = form.cleaned_data["curso"]
            group.cupo = form.cleaned_data["cupo"]
            group.save()
            for bloque_form in formset:
                bloque = bloque_form.save(commit=False)
                bloque.grupo = group
                bloque.save()
                bloque_form.save_m2m()  # Save the ManyToManyField data
            group.profesores.set(form.cleaned_data["profesores"])

            return HttpResponseRedirect(reverse_lazy('clases:list-groups'))
        else:
            print(form.errors)
    else:
        form_data = {
            'curso': group.curso,
            'profesores': group.profesores.all(),
            'cupo': group.cupo,
        }
        form = CreateGroupForm(initial=form_data)
        formset = BloqueDeClaseFormSet(queryset=BloqueDeClase.objects.filter(grupo=group))
        print(BloqueDeClase.objects.filter(grupo=group))

    return render(request, 'clases/create_grupo_form.html', {'form': form, 'formset': formset})

@login_required
def delete_group(request, pk):
    grupo = get_object_or_404(Grupo, id=pk)
    print(grupo.__dict__)

    if request.method == 'POST':
        grupo.delete()
        return redirect(reverse_lazy('clases:list-groups'))
    return render(request, 'clases/grupo_confirm_delete.html', {'grupo': grupo})

@login_required
def detail_group(request, pk):
    grupo = get_object_or_404(Grupo, id=pk)
    print(grupo.__dict__)
    return render(request, 'clases/grupo_detail.html', {'grupo': grupo})

def list_groups(request):
    grupos = Grupo.objects.all()
    return render(request, 'clases/grupo_list.html', {'lista_grupos': grupos})

def load_professors(request):
    curso_id = request.GET.get('curso')
    profesores = Profesor.objects.filter(cursos__id=curso_id)
    return render(request, 'clases/profesores_options.html', {'profesores': profesores})