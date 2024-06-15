from datetime import datetime
from django import forms
from domain.models import Curso,Salon,Profesor,Dia


class CreateGroupForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(),
                                  widget=forms.Select(attrs={"hx-get":"cargar-profesores/","hx-target":"#id_profesores"}) )
    profesores = forms.ModelMultipleChoiceField(queryset=Profesor.objects.none())
    cupo = forms.IntegerField(min_value=0, max_value=500)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["curso"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700 "})
        self.fields["profesores"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
        self.fields["cupo"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700", "min": "0", "max": "500"})
        if "curso" in self.data:
            curso_id = int(self.data.get("curso"))
            self.fields["profesores"].queryset = Profesor.objects.filter(cursos__id=curso_id).order_by("nombre")
        elif self.initial and 'curso' in self.initial:
            print(f"THERE IS AN INITIAL VALUE:  {self.initial} " )
            curso_id = self.initial['curso'].id
            self.fields["profesores"].queryset = Profesor.objects.filter(cursos__id=curso_id).order_by("nombre")


class BloqueDeClaseForm(forms.Form):
    dia = forms.ModelMultipleChoiceField(queryset=Dia.objects.all(), widget=forms.SelectMultiple(attrs={"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"}))
    hora_inicio = forms.ChoiceField(choices=[(f'{i//2:02d}:{i%2*30:02d}', f'{i//2:02d}:{i%2*30:02d}') for i in range(48)],widget=forms.Select(attrs={"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"}))
    hora_fin = forms.ChoiceField(choices=[(f'{i//2:02d}:{i%2*30:02d}', f'{i//2:02d}:{i%2*30:02d}') for i in range(48)],widget=forms.Select(attrs={"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"}))
    salon = forms.ModelChoiceField(queryset=Salon.objects.all(),widget=forms.Select(attrs={"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"}))

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        print(f"INSTANCE: {self.instance}")
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['dia'].initial = self.instance.dia.all()
            self.fields['hora_inicio'].initial = self.instance.hora_inicio.strftime('%H:%M')
            self.fields['hora_fin'].initial = self.instance.hora_fin.strftime('%H:%M')
            self.fields['salon'].initial = self.instance.salon

BloqueFormSet = forms.formset_factory(BloqueDeClaseForm)