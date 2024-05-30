from django.forms import ModelForm, TextInput, Textarea, NumberInput, SelectMultiple
from domain.models import Carrera

class CreateCareerForm(ModelForm):
    class Meta:
        model = Carrera
        fields = ['nombre', 'descripcion', 'duracion_meses', 'cursos']
        widgets = {
            'nombre': TextInput(attrs={
                'class': "block mb-2 text-sm font-medium text-white w-full",
                'placeholder': 'Ingresa el nombre de la carrera...'
                }),
            'descripcion': Textarea(attrs={
                'class': "block p-2.5 w-full text-sm bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 text-white dark:focus:ring-blue-500 dark:focus:border-blue-500", 
                'placeholder': 'Añade una descripción significativa...'
                }),
            'duracion_meses': NumberInput(attrs={
                'class': "block mb-2 text-sm font-medium text-white w-full", 
                'placeholder': 'Description'
                }),
            'cursos': SelectMultiple(attrs={
                'class': "block mb-2 text-sm font-medium text-white w-full rounded bg-gray-900", 
                'placeholder': 'Description'
                })
        }