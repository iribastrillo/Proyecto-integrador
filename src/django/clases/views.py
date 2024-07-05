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


# class CreateBloqueDeClase(LoginRequiredMixin, CreateView):
#     model = BloqueDeClase
#     form_class = BloqueDeClaseForm
#     template_name = 'clases/clases_form.html'
#     success_url = reverse_lazy('clases:home-class-blocks')

class ListBloqueDeClases (LoginRequiredMixin, ListView):
    model = BloqueDeClase
    template_name = 'clases/clases_list.html'
    context_object_name='lista_clases'


class DetailBloqueDeClase(LoginRequiredMixin, DetailView):
    model = BloqueDeClase
    template_name = 'clases/clases_list.html'


class DeleteBloqueDeClase(LoginRequiredMixin, DeleteView):
    model = BloqueDeClase
    # template_name = 'clases/partials/bloque_clase_delete_form_partial.html'
    template_name = 'clases/clases_confirm_delete.html'
    # form_class = BloqueDeClaseForm
    # success_url = reverse_lazy('clases:list-groups')

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
def create_group(request):
    print(f"request post cleaned:{request.POST}")

    BloqueDeClaseFormSet = formset_factory(BloqueDeClaseForm )
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        formset = BloqueDeClaseFormSet(request.POST)
        print(f"Formset management form {formset.management_form}")

        print(f"FORMSETT EN CREATE GROUP : {formset}")
        if form.is_valid() and formset.is_valid():
            curso = form.cleaned_data["curso"]
            profesores = form.cleaned_data["profesores"]
            cupo = form.cleaned_data["cupo"]
            grupo = Grupo(curso=curso, cupo=cupo)
            grupo.save()

            for bloque_form in formset:
                print(f"bloque form : {bloque_form.cleaned_data}")
                hora_inicio = datetime.strptime(bloque_form.cleaned_data['hora_inicio'], '%H:%M').time()
                hora_fin = datetime.strptime(bloque_form.cleaned_data['hora_fin'], '%H:%M').time()
                salon = bloque_form.cleaned_data['salon']

                bloque = BloqueDeClase(hora_inicio=hora_inicio, hora_fin=hora_fin, salon=salon, grupo=grupo)
                bloque.save()
                bloque.dia.set(bloque_form.cleaned_data['dia'])  # Use .set() for ManyToManyField

            grupo.profesores.set(profesores)
            return HttpResponseRedirect(reverse_lazy('clases:list-groups'))
        else:
            print(form.errors)
    else:
        form = CreateGroupForm()
        formset = BloqueDeClaseFormSet()
    print(f"View management form  formset:{ formset.management_form}")
    return render(request, 'clases/create_grupo_form.html', {'form': form, 'formset': formset})

def new_form(request: HttpRequest):
    print("SE CLICKEA AGREGAR BLOQUE DE CLASE")
    form = BloqueDeClase()
    context = {
        "form": form
    }
    return render(request, "partials/clase_form.html", context)

@login_required
def update_group(request, pk):
    group = get_object_or_404(Grupo, id=pk)
    bloque_de_clase_instances = BloqueDeClase.objects.filter(grupo=group)
    print(f"Bloques de clase en update group {bloque_de_clase_instances}")

    if request.method == 'POST':
        print("REQUEST IS POST in update group")
        print(request.POST)
        form = CreateGroupForm(request.POST)
        # formset = [BloqueDeClaseForm(request.POST, prefix=str(i), instance=bloque) for i, bloque in enumerate(bloque_de_clase_instances)]
        formset = [BloqueDeClaseForm(request.POST, prefix=str(form), instance=bloque) for i, bloque in enumerate(bloque_de_clase_instances)]
        if form.is_valid() and all([f.is_valid() for f in formset]):
            group.curso = form.cleaned_data["curso"]
            group.cupo = form.cleaned_data["cupo"]
            group.save()

            for f in formset:

                print(f"FORMSET IS VALID: {f.cleaned_data}")
                bloque = f.instance if f.instance else BloqueDeClase()
                bloque.hora_inicio = datetime.strptime(f.cleaned_data['hora_inicio'], '%H:%M').time()
                bloque.hora_fin = datetime.strptime(f.cleaned_data['hora_fin'], '%H:%M').time()
                bloque.salon = f.cleaned_data['salon']
                bloque.grupo = group
                bloque.save()
                bloque.dia.set(f.cleaned_data['dia']) # Use .set() for ManyToManyField

            group.profesores.set(form.cleaned_data["profesores"])

            return HttpResponseRedirect(reverse_lazy('clases:list-groups'))
        else:
            print(f"form errors: {form.errors}")
    else:
        form_data = {
            'curso': group.curso,
            'profesores': group.profesores.all(),
            'cupo': group.cupo,
        }
        form = CreateGroupForm(initial=form_data)
        formset = [BloqueDeClaseForm(request.POST or None, prefix=str(i), instance=bloque) for i, bloque in enumerate(bloque_de_clase_instances)]


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

def add_block_class_form(request):
    if request=='POST':
        pass
    form=BloqueDeClaseForm(prefix='formset', auto_id=False)
    return render(request, 'clases/components/bloque_component.html', {'form': form})




# https://stackoverflow.com/questions/74757197/the-right-way-to-dynamically-add-django-formset-instances-and-post-usign-htmx/74924295#74924295
def formset_view(request):
    template = 'bloque_component.html'

    if request.POST:
        formset = BloqueFormSet(request.POST)
        if formset.is_valid():
            print(f">>>> form is valid. Request.post is {request.POST}")
            return HttpResponseRedirect(reverse('clases:formset-view'))
    else:
        formset = BloqueFormSet()

    return render(request, template, {'formset': formset})


def add_formset(request, current_total_formsets):
    new_formset = build_new_formset(BloqueFormSet(), current_total_formsets)
    context = {
        'new_formset': new_formset,
        'new_total_formsets': current_total_formsets + 1,
    }
    return render(request, 'clases/partials/formset_partial.html', context)

# Helper to build the needed formset
def build_new_formset(formset, new_total_formsets):
    html = ""

    for form in formset.empty_form:
        html += f'<div class="flex flex-col mb-4">'
        html += form.label_tag().replace('__prefix__', str(new_total_formsets))
        html += str(form).replace('__prefix__', str(new_total_formsets))
        html += '</div>'
    return mark_safe(html)

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
    # success_url = reverse_lazy('clases:list-groups')


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
                    # grupo = Grupo.objects.get(pk=self.kwargs['pk'])
                    # context = {
                    #     'form': form,
                    #     'grupo': grupo,

                    # }
                    # return self.render_to_response(context)
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
        print(f"Update bloque de clase ")
        print(f"self object pk {self.object.pk}")
        context = super(BloqueClaseUpdateView,self).get_context_data(**kwargs)
        grupo = self.object.grupo
        print(f"Grupo pk: {grupo.pk}")
        print(f" Context: {context}")
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
