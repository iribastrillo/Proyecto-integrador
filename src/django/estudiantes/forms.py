from django import forms
from django.urls import reverse_lazy

from domain.models import Grupo
from .validators import group_is_not_full


class InscripcionForm(forms.Form):
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "hx-target": "#group-info",
                "hx-get": reverse_lazy("clases:load-group"),
            }
        ),
        validators=[group_is_not_full],
    )


class BajaForm(forms.Form):
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
