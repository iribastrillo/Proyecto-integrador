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
        self.fields["curso"].widget.attrs.update(
            {"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700 "}
        )
        self.fields["profesores"].widget.attrs.update(
            {"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"}
        )
        self.fields["cupo"].widget.attrs.update(
            {
                "class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700",
                "min": "0",
                "max": "500",
            }
        )
        if "curso" in self.data:
            curso_id = int(self.data.get("curso"))
            self.fields["profesores"].queryset = Profesor.objects.filter(cursos__id=curso_id).order_by("nombre")
        elif self.initial and 'curso' in self.initial:
            print(f"THERE IS AN INITIAL VALUE:  {self.initial} " )
            # curso_id = self.initial['curso'].id
            curso_id = self.initial['curso']
            self.fields["profesores"].queryset = Profesor.objects.filter(cursos__id=curso_id).order_by("nombre")


class BloqueDeClaseForm(forms.ModelForm):
    class Meta:
        model=BloqueDeClase
        fields=["dia","hora_inicio","hora_fin","salon","id"]
    dia = forms.ModelMultipleChoiceField(queryset=Dia.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"class": "bg-gray-900   shadow dark:bg-gray-900","hx-trigger":"change","hx-include":"[name='salon'],[name='hora_inicio'],[name='hora_fin'],[name='dia'],[name='id'],input[type='checkbox']:checked", "hx-get":"cargar-horas-disponibles/","hx-target":"#id_hora_inicio","hx-select-oob":"#id_hora_fin"}), required=True)
    hora_inicio = forms.ChoiceField(choices=[(f'{i//2:02d}:{i%2*30:02d}', f'{i//2:02d}:{i%2*30:02d}') for i in range(48)],widget=forms.Select(attrs={"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700","id":"id_hora_inicio"}), required=True)
    hora_fin = forms.ChoiceField(choices=[(f'{i//2:02d}:{i%2*30:02d}', f'{i//2:02d}:{i%2*30:02d}') for i in range(48)],widget=forms.Select(attrs={"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700","id":"id_hora_fin"}), required=True)
    salon = forms.ModelChoiceField(queryset=Salon.objects.all(),widget=forms.Select(attrs={"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-900", "hx-get":"cargar-horas-disponibles/","hx-target":"#id_hora_inicio","hx-select-oob":"#id_hora_fin","hx-include":"[name='dia'],[name='salon'],[name='hora_inicio'],[name='hora_fin'],[name='id']"}), required=True)
    id = forms.CharField(widget=forms.HiddenInput(), required=False)


    def clean(self):
        cleaned_data = super().clean()
        dias = cleaned_data.get("dia")
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")
        salon = cleaned_data.get("salon")
        print(f"cleaned data {cleaned_data}")
        # Check if a block already exists for the same day, salon, and overlapping time range
        if hora_fin <= hora_inicio:
            raise forms.ValidationError("La hora de fin debe ser mayor a la hora de inicio")
        # return hora_fin
        try:
            bloque_ya_ocupado = BloqueDeClase.objects.get(
                dia__in=dias,  # Use '__in' to handle multiple selected days
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
                salon=salon,
            )
            raise forms.ValidationError(
                "Ya existe una clase creada para el salón y el horario seleccionado. desde Forms"
            )
        except BloqueDeClase.DoesNotExist:
            # No existing block found, continue with form submission
            pass

        return cleaned_data


    def __init__(self, *args, **kwargs):
        super(BloqueDeClaseForm,self).__init__(*args, **kwargs)
        if self.initial:
            self.initial['hora_inicio'] =self.initial['hora_inicio'].strftime('%H:%M')
            self.initial['hora_fin'] = self.initial['hora_fin'].strftime('%H:%M')

            self.fields["id"] = forms.CharField(widget=forms.HiddenInput(), initial=self.initial['id'])
            print(f"bloque_Clase_id {self.initial['id']}")




