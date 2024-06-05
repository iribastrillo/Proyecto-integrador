from django import forms
from domain.models import Curso,Salon,Alumno,BloqueDeClase,Profesor

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

class BloqueDeClaseForm(forms.ModelForm):
    class Meta:
        model = BloqueDeClase
        fields = [ 'dia', 'hora_inicio', 'hora_fin', 'salon','grupo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        WEEKDAYS=[
            ('Lunes', 'Lunes'),
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