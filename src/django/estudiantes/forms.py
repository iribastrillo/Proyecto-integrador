from django import forms
from django.urls import reverse_lazy

from domain.models import Grupo
from django.core.validators import MaxValueValidator, MinValueValidator

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
    fee = forms.DecimalField(
        required=True,
        validators=[
            MinValueValidator(0, "La cuota real debe ser mayor que 0."),
            MaxValueValidator(50000, "La cuota real debe ser menor a 50000."),
        ],
    )


class BajaForm(forms.Form):
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
