from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from domain.models import BloqueDeClase,Grupo,Profesor,Salon
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory,formset_factory
from .forms import CreateGroupForm, BloqueDeClaseForm
from datetime import datetime
from django.utils.safestring import mark_safe
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class ListBloqueDeClases (LoginRequiredMixin, ListView):
    model = BloqueDeClase
    template_name = 'clases/clases_list.html'
    context_object_name='lista_clases'


class DetailBloqueDeClase(LoginRequiredMixin, DetailView):
    model = BloqueDeClase
    template_name = 'clases/clases_list.html'


class DeleteBloqueDeClase(LoginRequiredMixin, DeleteView):
    model = BloqueDeClase
    template_name = 'clases/clases_confirm_delete.html'

    def get_success_url(self):
        print("Success url")
        return reverse("clases:detail-group", kwargs={"pk": self.get_object().grupo.pk})

    def get_context_data(self, **kwargs):
        context = super(DeleteBloqueDeClase,self).get_context_data(**kwargs)
        # Retrieve the BloqueDeClase instance being deleted
        bloque_de_clase = self.get_object()
        # Add the instance data to the context
        context['bloque'] = bloque_de_clase
        context['grupo_pk'] = bloque_de_clase.grupo.pk
        return context


@login_required
def delete_group(request, pk):
    grupo = get_object_or_404(Grupo, id=pk)
    print(grupo.__dict__)

    if request.method == 'POST':
        grupo.delete()
        return redirect(reverse_lazy('clases:list-groups'))
    return render(request, 'clases/grupo_confirm_delete.html', {'grupo': grupo})

def list_groups(request):
    grupos = Grupo.objects.all()
    for grupo in grupos:
        print(grupo.__dict__)
    return render(request, 'clases/grupo_list.html', {'lista_grupos': grupos})

def load_professors(request):
    curso_id = request.GET.get('curso')
    profesores = Profesor.objects.filter(cursos__id=curso_id)
    return render(request, 'clases/profesores_options.html', {'profesores': profesores})

def load_group(request):
    id_grupo = request.GET.get('grupo')
    grupo = Grupo.objects.get (pk=id_grupo)
    return render(request, 'clases/partials/info_grupo_enrolment_modal.html', {'grupo': grupo})

class CreateGrupo(LoginRequiredMixin, CreateView):
    model = Grupo
    form_class=CreateGroupForm
    template_name='clases/grupo_form.html'
    success_message = "Se agregó grupo con éxito"
    def get_success_url(self):
        return reverse_lazy("clases:detail-group", kwargs={"pk": self.object.group.pk})


    def form_valid(self, form):
        print("form valid")
        # Save the form and get the newly created instance
        curso = form.cleaned_data["curso"]
        profesores = form.cleaned_data["profesores"]
        cupo = form.cleaned_data["cupo"]
        grupo = Grupo(curso=curso, cupo=cupo)
        grupo.save()
        grupo.profesores.set(profesores)
        print(grupo.pk)
        print(f"Cantidad de alumnos en el grupo: {len(grupo.alumnos.all())}")

        return redirect('clases:list-groups')
    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class UpdateGrupo(LoginRequiredMixin, UpdateView):
    model = Grupo  # Specify the model here
    form_class=CreateGroupForm
    template_name='clases/grupo_form.html'
    success_message = "Se agregó grupo con éxito"
    def get_success_url(self):
        return reverse_lazy("clases:detail-group", kwargs={"pk": self.get_object().pk})

class GrupoDetailView(LoginRequiredMixin,DetailView):
    model = Grupo
    context_object_name = 'grupo'
    template_name = 'clases/grupo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupo = self.object  # Get the current Grupo instance
        context['bloques_de_clase'] = BloqueDeClase.objects.filter(grupo=grupo)
        print(f"Bloques de clases encontrados: {context['bloques_de_clase']}")
        return context

class CreateBloqueDeClase(LoginRequiredMixin,CreateView):
    print(f"Create bloque de clase ")
    model_name=BloqueDeClase
    # template_name = 'clases/bloque_clase_form.html'
    template_name = 'clases/partials/bloque_clase_form_partial.html'
    form_class = BloqueDeClaseForm

    def get (self, request, *args, **kwargs):
        form = self.form_class()
        grupo = Grupo.objects.get (pk = kwargs['pk'])
        context = {
            'form': form,
            'grupo': grupo
        }
        return render (request, self.template_name, context)


    def post (self, request, *args, **kwargs):
        form = BloqueDeClaseForm (request.POST)
        grupo = Grupo.objects.get(pk=kwargs["pk"])
        print(f"Creando bloque de clase para el grupo {grupo.pk}")
        if form.is_valid():
            print("Form is valid")
            # grupo = form.cleaned_data["grupo"]
            dias = form.cleaned_data["dia"]
            hora_inicio = form.cleaned_data["hora_inicio"]
            hora_fin = form.cleaned_data["hora_fin"]
            salon = form.cleaned_data["salon"]
            print(f"BLOQUE A SER CREADO los dias: {dias} hora_inicio: {hora_inicio} hora_fin: {hora_fin} salon: {salon}")

            for dia_obj in dias.all():
                try:
                    bloque_ya_ocupado = BloqueDeClase.objects.get(
                        dia=dia_obj,
                        hora_inicio__lt=hora_fin,
                        hora_fin__gt=hora_inicio,
                        salon=salon
                )
                    print(f"Bloque ya ocupado {dia_obj}: {bloque_ya_ocupado}")
                    messages.add_message(request, messages.ERROR, "Ya existe una clase creada para el salon y el horario seleccionado.")
                    return HttpResponse()

                except BloqueDeClase.DoesNotExist:
                # Continue to the next day
                 pass

            bloque = BloqueDeClase.objects.create(
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                salon=salon,
                grupo=grupo
            )

            bloque.dia.set(dias)
            bloque.save()
            print(f"Bloque creado: {bloque}")
            messages.add_message (request, messages.SUCCESS, f"Clase creada con exito.")
            return HttpResponse()
        else:
            print("form invalid")
            messages.add_message (request, messages.ERROR, "Ha habido un error")
            grupo = Grupo.objects.get(pk=self.kwargs['pk'])
            context = {
                'form': form,
                'grupo': grupo
            }
            return self.render_to_response(context)


class BloqueClaseUpdateView(LoginRequiredMixin, UpdateView):
    model = BloqueDeClase
    template_name = 'clases/partials/bloque_clase_update_form_partial.html'
    # form_class = UpdateBloqueDeClaseForm
    form_class = BloqueDeClaseForm

    def get_context_data(self, **kwargs):
        context = super(BloqueClaseUpdateView,self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        grupo = self.object.grupo
        dias = form.cleaned_data["dia"]
        hora_inicio = form.cleaned_data["hora_inicio"]
        hora_fin = form.cleaned_data["hora_fin"]
        salon = form.cleaned_data["salon"]

        for dia_obj in dias.all():
            try:

                bloque_ya_ocupado = BloqueDeClase.objects.get(
                        dia=dia_obj,
                        hora_inicio__lt=hora_fin,
                        hora_fin__gt=hora_inicio,
                        salon=salon,
                        grupo=grupo
                    )
                if bloque_ya_ocupado != self.object:
                    messages.add_message(self.request, messages.ERROR, "Ya existe una clase creada para el salon y el horario seleccionado.")
                    return self.form_invalid(form)
            except BloqueDeClase.DoesNotExist:
                    # Continue to the next day
                    pass
        # Save the updated form
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clases:detail-group', kwargs={'pk': self.object.grupo.pk})

def crear_bloque_de_clase(request,pk=None):
    grupo = get_object_or_404(Grupo, pk=pk)

    if request.method=='POST':
        form = BloqueDeClaseForm(request.POST or None)
        if form.is_valid():
            bloque=form.save(commit=False)
            bloque.grupo=grupo
            bloque.save()
            context={'bloque':bloque}
            return render()

def load_horas_disponibles(request):
    salon_id = request.GET.get('salon')
    dia=request.GET.get('dia')
    bloques = BloqueDeClase.objects.filter(salon__id=salon_id, dia__name=dia)
    horas_no_disponibles = [(bloque.hora_inicio, bloque.hora_fin) for bloque in bloques]
    return render(request, 'clases/horas_options.html', {'horas': horas_no_disponibles})
