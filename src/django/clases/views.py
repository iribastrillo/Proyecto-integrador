from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from domain.models import BloqueDeClase,Grupo
from django.urls import reverse, reverse_lazy
from domain.models import Profesor
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory,formset_factory
from .forms import CreateGroupForm, BloqueDeClaseForm, BloqueFormSet
from datetime import datetime
from django.utils.safestring import mark_safe


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
    template_name = 'clases/confirm_delete.html'
    success_url=reverse_lazy('clases:list-class-blocks')


class UpdateBloqueDeClase(LoginRequiredMixin, UpdateView):
    model=BloqueDeClase
    # fields = ['curso', 'alumnos_cursos', 'cupo', 'profesores', 'dia', 'duracion', 'hora_inicio', 'hora_fin', 'salon']
    template_name = 'clases/confirm_delete.html'
    success_url=reverse_lazy('clases:list-class-blocks')

@login_required
def create_group(request):
    print(f"request post cleaned:{request.POST}")

    BloqueDeClaseFormSet = formset_factory(BloqueDeClaseForm )
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        formset = BloqueDeClaseFormSet(request.POST)
        print(f"Formset management form {formset.management_form}")

        # print(f"FORMSETT EN CREATE GROUP : {formset}")
        if form.is_valid() and formset.is_valid():
            curso = form.cleaned_data["curso"]
            profesores = form.cleaned_data["profesores"]
            cupo = form.cleaned_data["cupo"]
            groupo = Grupo(curso=curso, cupo=cupo)
            groupo.save()

            for bloque_form in formset:
                print(f"bloque form : {bloque_form.cleaned_data}")
                hora_inicio = datetime.strptime(bloque_form.cleaned_data['hora_inicio'], '%H:%M').time()
                hora_fin = datetime.strptime(bloque_form.cleaned_data['hora_fin'], '%H:%M').time()
                salon = bloque_form.cleaned_data['salon']

                bloque = BloqueDeClase(hora_inicio=hora_inicio, hora_fin=hora_fin, salon=salon, grupo=groupo)
                bloque.save()
                bloque.dia.set(bloque_form.cleaned_data['dia'])  # Use .set() for ManyToManyField

            groupo.profesores.set(profesores)
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
    print(f"Bloques de clase  {bloque_de_clase_instances}")

    if request.method == 'POST':
        print("REQUEST IS POST")
        print(request.POST)
        form = CreateGroupForm(request.POST)
        formset = [BloqueDeClaseForm(request.POST, prefix=str(i), instance=bloque) for i, bloque in enumerate(bloque_de_clase_instances)]
        print(f"FORMSETT EN UPDATE GROUP : {formset}")
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
            print(form.errors)
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
        html += form.label_tag().replace('__prefix__', str(new_total_formsets))
        html += str(form).replace('__prefix__', str(new_total_formsets))

    return mark_safe(html)

class CreateGrupo(LoginRequiredMixin, CreateView):
    
    model = Grupo  # Specify the model here
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
    # Here you can add your logic to handle validation errors
        return render(self.request, self.template_name, {'form': form})

class GrupoDetailView(LoginRequiredMixin,DetailView):
    model = Grupo
    context_object_name = 'grupo'
    template_name = 'grupo/grupo_detail.html'              

class CreateBloqueDeClase(LoginRequiredMixin,CreateView):
    print(f"Create bloque de clase ")
    model_name=BloqueDeClase
    template_name = 'clases/bloque/bloque_clase_form.html'
    form_class = BloqueDeClaseForm
    success_url = reverse_lazy('clases:list-groups')

    def form_valid(self, form):
        # Custom logic when the form is valid (e.g., save data)
        # For example:
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        # Save data or perform other actions
        # ...

        return super().form_valid(form)