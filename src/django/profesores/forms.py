import datetime
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from domain.models import Grupo,FaltaProfesor,Profesor

class FaltaProfesorForm(forms.ModelForm):
    class Meta:
        model = FaltaProfesor
        fields = ['profesor_titular','profesor_suplente','fecha','grupo','descripcion']
        exclude = ['profesor_titular']

    def __init__(self, *args, **kwargs):
        super(FaltaProfesorForm, self).__init__(*args, **kwargs)
        # self.fields['profesor_titular'].queryset = Profesor.objects.all()
        self.fields['profesor_suplente'].queryset = Profesor.objects.all()
        self.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields["fecha"].widget.attrs.update(
        {"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"}
        )
        self.fields['grupo'].queryset = Grupo.objects.all()
        self.fields['descripcion'].widget = forms.Textarea(attrs={'rows': 4, 'cols': 15})
        if 'grupo' in self.initial:
            self.fields['grupo'].queryset =self.initial['grupo']


    def clean(self) -> Any:
        cleaned_data = super().clean()
        profesor_suplente = cleaned_data.get("profesor_suplente")
        grupo = cleaned_data.get("grupo")
        if grupo.curso not in profesor_suplente.cursos.all():
            raise ValidationError('El profesor seleccionado no puede dar ese curso')
        return cleaned_data

