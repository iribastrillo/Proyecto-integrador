from django import forms

from domain.models import AlumnoCurso


class InscripcionForm(forms.ModelForm):
    
    class Meta:
        model = AlumnoCurso
        fields = ["alumno", "curso"]

    