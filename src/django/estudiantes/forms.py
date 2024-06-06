from django import forms

from domain.models import Grupo
from .validators import group_is_not_full

class InscripcionForm(forms.Form):
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'}),
        validators=[group_is_not_full]
    )

    