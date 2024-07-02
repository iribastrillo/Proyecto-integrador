from datetime import datetime
from django import forms
from domain.models import Curso,Salon,Profesor,Dia,Grupo,BloqueDeClase


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model=Grupo
        fields=["curso","profesores","cupo"]
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
# class CreateGroupForm(forms.Form):
#     curso = forms.ModelChoiceField(queryset=Curso.objects.all(),
#                                   widget=forms.Select(attrs={"hx-get":"cargar-profesores/","hx-target":"#id_profesores"}) )
#     profesores = forms.ModelMultipleChoiceField(queryset=Profesor.objects.none())
#     cupo = forms.IntegerField(min_value=0, max_value=500)
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["curso"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700 "})
#         self.fields["profesores"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
#         self.fields["cupo"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700", "min": "0", "max": "500"})
#         if "curso" in self.data:
#             curso_id = int(self.data.get("curso"))
#             self.fields["profesores"].queryset = Profesor.objects.filter(cursos__id=curso_id).order_by("nombre")
#         elif self.initial and 'curso' in self.initial:
#             print(f"THERE IS AN INITIAL VALUE:  {self.initial} " )
#             curso_id = self.initial['curso'].id
#             self.fields["profesores"].queryset = Profesor.objects.filter(cursos__id=curso_id).order_by("nombre")


class BloqueDeClaseForm(forms.ModelForm):
    class Meta:
        model=BloqueDeClase
        fields=["dia","hora_inicio","hora_fin","salon"]
    dia = forms.ModelMultipleChoiceField(queryset=Dia.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"class": "bg-gray-900   shadow dark:bg-gray-700"}))
    hora_inicio = forms.ChoiceField(choices=[(f'{i//2:02d}:{i%2*30:02d}', f'{i//2:02d}:{i%2*30:02d}') for i in range(48)],widget=forms.Select(attrs={"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"}))
    hora_fin = forms.ChoiceField(choices=[(f'{i//2:02d}:{i%2*30:02d}', f'{i//2:02d}:{i%2*30:02d}') for i in range(48)],widget=forms.Select(attrs={"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"}))
    salon = forms.ModelChoiceField(queryset=Salon.objects.all(),widget=forms.Select(attrs={"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"}))

    def __init__(self, *args, **kwargs):
        super(BloqueDeClaseForm,self).__init__(*args, **kwargs)       
        if self.initial:
            self.initial['hora_inicio'] =self.initial['hora_inicio'].strftime('%H:%M')
            self.initial['hora_fin'] = self.initial['hora_fin'].strftime('%H:%M')


BloqueFormSet = forms.formset_factory(BloqueDeClaseForm)