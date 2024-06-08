from datetime import datetime
from django import forms
from domain.models import Curso,Salon,Alumno,BloqueDeClase,Profesor,Dia

class CreateGroupForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(),
                                  widget=forms.Select(attrs={"hx-get":"cargar-profesores/","hx-target":"#id_profesores"}) )

    # alumnos = forms.ModelMultipleChoiceField(queryset=Alumno.objects.all())
    profesores = forms.ModelMultipleChoiceField(queryset=Profesor.objects.none())
    cupo = forms.IntegerField(min_value=0, max_value=500)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["curso"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700 "})
        # self.fields["alumnos"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
        self.fields["profesores"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
        self.fields["cupo"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700", "min": "0", "max": "500"})
        if "curso" in self.data:
            curso_id = int(self.data.get("curso"))
            self.fields["profesores"].queryset = Profesor.objects.filter(cursos__id=curso_id).order_by("nombre")
        elif self.initial and 'curso' in self.initial:
            print(f"THERE IS AN INITIAL VALUE:  {self.initial} " )
            curso_id = self.initial['curso'].id
            self.fields["profesores"].queryset = Profesor.objects.filter(cursos__id=curso_id).order_by("nombre")


class BloqueDeClaseForm(forms.ModelForm):
    class Meta:
        model = BloqueDeClase
        fields = [ 'dia', 'hora_inicio', 'hora_fin', 'salon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # WEEKDAYS=[
        #     ('Lunes', 'Lunes'),
        #     ('Martes', 'Martes'),
        #     ('Miercoles', 'Miercoles'),
        #     ('Jueves', 'Jueves'),
        #     ('Viernes', 'Viernes'),
        #     ('Sabado', 'Sabado'),
        #     ('Domingo', 'Domingos')
        #     ]
        # DIAS = list(WEEKDAYS)
        # DIAS.insert(0, ('', 'Seleccione opción'))
        self.fields["dia"]=forms.ModelMultipleChoiceField(queryset=Dia.objects.all())
        self.fields["dia"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
        SALONES = list(Salon.objects.values_list('id', 'nombre'))
        SALONES.insert(0, ('', 'Seleccione opción'))
        self.fields["salon"]=forms.ModelChoiceField(queryset=Salon.objects.all())
        self.fields["salon"].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
        # HOURS = [(f'{i//2:02d}:{i%2*30:02d}', f'{i//2:02d}:{i%2*30:02d}') for i in range(48)]
        HOURS = [(f'{i//2:02d}:{i%2*30:02d}:00', f'{i//2:02d}:{i%2*30:02d}:00') for i in range(48)]
        self.fields['hora_inicio'] = forms.ChoiceField(choices=HOURS)
        self.fields['hora_inicio'].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})
        self.fields['hora_fin'] = forms.ChoiceField(choices=HOURS)
        self.fields['hora_fin'].widget.attrs.update({"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"})

        # Set the initial value for each ChoiceField
        # if self.instance.pk:  # Check if this is an existing instance

        #     print("THERE IS AN INSTANCE OF THE BLOQUE")
        #     print(self.instance.dia)
        #     # self.fields['dia'].initial = self.instance.dia
        #     self.fields['hora_inicio'].initial = self.instance.hora_inicio.strftime('%H:%M')
        #     self.fields['hora_fin'].initial = self.instance.hora_inicio.strftime('%H:%M')
        #      # self.fields['salon'].initial = self.instance.salon
        #     print("Choices:", self.fields['hora_inicio'].choices)
        #     print("Initial value:", self.fields['hora_inicio'].initial)
        #     print(f"Converted Initial value: {self.instance.hora_inicio.strftime('%H:%M')}")


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
