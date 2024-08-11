import datetime
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from domain.models import Grupo,FaltaProfesor,Profesor

class FaltaProfesorForm(forms.ModelForm):
    class Meta:
        model = FaltaProfesor
        fields = ['profesor_titular','profesor_suplente','fecha','grupo','descripcion']

    grupo = forms.ModelChoiceField(queryset=Profesor.objects.all(),
                                  widget=forms.Select(attrs={"hx-get":"cargar-profesores/","hx-include":"[name='profesor_titular']","hx-target":"#id_profesor_suplente"}) )
    def __init__(self, *args, **kwargs):
        super(FaltaProfesorForm, self).__init__(*args, **kwargs)
        self.fields['profesor_suplente'].queryset = Profesor.objects.all()
        self.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields["fecha"].widget.attrs.update(
        {"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"}
        )
        self.fields['profesor_titular'].widget = forms.HiddenInput()
        self.fields['grupo'].queryset = Grupo.objects.filter(activo=True)

        if(initial:=kwargs.get('initial')):
            if 'profesor_titular' in initial:
                self.fields['profesor_titular'].widget = forms.HiddenInput(attrs={'value': initial['profesor_titular']})
        self.fields['descripcion'].widget = forms.Textarea(attrs={'rows': 4, 'cols': 15})
        if 'grupo' in self.initial:
            self.fields['grupo'].queryset = Grupo.objects.filter(profesores__pk=self.initial['profesor_titular'], activo=True)
            self.initial['grupo'] = self.initial['grupo']
        if 'profesor_suplente' in self.initial:
            grupo=Grupo.objects.get(pk=self.initial['grupo'])
            self.fields['profesor_suplente'].queryset = Profesor.objects.filter(cursos__nombre=grupo.curso.nombre).exclude(pk=self.initial['profesor_titular'])
            if 'profesor_suplente' in self.initial:
                self.initial['profesor_suplente'] = self.initial['profesor_suplente']
        if 'fecha' in self.initial:
            self.initial['fecha']=self.initial['fecha'].strftime('%Y-%m-%d')
        if 'descripcion' in self.initial:
            self.initial['descripcion']=self.initial['descripcion']


    def clean(self) -> Any:
        cleaned_data = super().clean()
        print(f"cleaned_data {cleaned_data}")
        grupo = cleaned_data.get("grupo")
        profesor_suplente = cleaned_data.get("profesor_suplente")
        if profesor_suplente:
            if grupo.curso not in profesor_suplente.cursos.all():
                raise ValidationError('El profesor seleccionado no puede dar ese curso')
        if grupo.curso not in cleaned_data.get("profesor_titular").cursos.all():
            raise ValidationError('El profesor titular no pertenece al curso seleccionado')
        profesor_titutar = cleaned_data.get("profesor_titular")
        faltas = FaltaProfesor.objects.filter(profesor_titular=profesor_titutar, fecha=cleaned_data.get("fecha"), grupo=grupo).exclude(pk=self.instance.pk)
        if faltas.exists():
            raise ValidationError('Ya existe una falta para ese profesor en esa fecha y ese grupo')
        return cleaned_data


