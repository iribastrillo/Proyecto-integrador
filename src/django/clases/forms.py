from django import forms
from domain.models import Leccion,Curso,Salon,Alumno,BloqueDeClase,Profesor

class CreateLeccionForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(),
                                  widget=forms.Select(attrs={"hx-get":"cargar-profesores/","hx-target":"#id_profesores"}) )

    alumnos = forms.ModelMultipleChoiceField(queryset=Alumno.objects.all())
    profesores = forms.ModelMultipleChoiceField(queryset=Profesor.objects.none())
    salon = forms.ModelChoiceField(queryset=Salon.objects.all())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["curso"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700 "})
        self.fields["alumnos"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
        self.fields["profesores"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
        self.fields["salon"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
