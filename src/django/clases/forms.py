from django import forms
from domain.models import Leccion,Curso,Salon,Alumno,BloqueDeClase,Profesor

class CreateGroupForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(),
                                  widget=forms.Select(attrs={"hx-get":"cargar-profesores/","hx-target":"#id_profesores"}) )

    alumnos = forms.ModelMultipleChoiceField(queryset=Alumno.objects.all())
    profesores = forms.ModelMultipleChoiceField(queryset=Profesor.objects.none())
    cupo = forms.IntegerField(min_value=0, max_value=500)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["curso"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700 "})
        self.fields["alumnos"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
        self.fields["profesores"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
        self.fields["cupo"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700", "min": "0", "max": "500"})
        if "curso" in self.data:
            curso_id = int(self.data.get("curso"))
            self.fields["profesores"].queryset = Profesor.objects.filter(cursos__id=curso_id).order_by("nombre")
        if self.initial:
            if 'profesores' in self.initial:
                self.fields['profesores'].queryset = Profesor.objects.all()

