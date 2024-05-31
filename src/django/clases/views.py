from django.shortcuts import render
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from domain.models import BloqueDeClase
from django.urls import reverse_lazy
from django import forms
from domain.models import Curso,Salon

# Form view original
# class CreateBloqueDeClase (LoginRequiredMixin, CreateView):
#     model = BloqueDeClase
#     fields = ['curso', 'alumnos_cursos', 'cupo', 'profesores', 'dia', 'hora_inicio', 'hora_fin', 'salon']
#     template_name = 'clases/clases_form.html'
#     success_url=reverse_lazy('clases:home-class-blocks')

class BloqueDeClaseForm(forms.ModelForm):
    class Meta:
        model = BloqueDeClase
        fields = ['curso', 'alumnos_cursos', 'cupo', 'profesores', 'dia', 'hora_inicio', 'hora_fin', 'salon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CURSOS = list(Curso.objects.values_list('id', 'nombre'))
        CURSOS.insert(0, ('', 'Seleccione opción'))
        self.fields['curso'] = forms.ChoiceField(choices=CURSOS)
        self.fields["curso"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700","option": "Seleccione Curso"})

        self.fields["profesores"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
        WEEKDAYS=[('Lunes', 'Lunes'),
      ('Martes', 'Martes'),
      ('Miercoles', 'Miercoles'),
      ('Jueves', 'Jueves'),
      ('Viernes', 'Viernes'),
      ('Sabado', 'Sabado'),
      ('Domingo', 'Domingos')
      ]

        DIAS = list(WEEKDAYS)
        DIAS.insert(0, ('', 'Seleccione opción'))
        self.fields["dia"]=forms.ChoiceField(choices=DIAS)
        self.fields["dia"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})

        SALONES = list(Salon.objects.values_list('id', 'nombre'))
        SALONES.insert(0, ('', 'Seleccione opción'))
        self.fields["salon"]=forms.ChoiceField(choices=SALONES)
        self.fields["salon"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})

        ## Falta Validar Form

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

# class AddCourseToCareer (LoginRequiredMixin, UpdateView):
#     model = Carrera
#     fields = ['cursos']
#     template_name_suffix = '_add_course'

