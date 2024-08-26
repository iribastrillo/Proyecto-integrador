from typing import Any
from django import forms
from django.urls import reverse_lazy

from domain.models import Grupo
from profiles.models import Alumno
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class InscripcionForm(forms.Form):
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "hx-target": "#enrolment-modal-info",
                "hx-get": reverse_lazy("clases:load-group"),
            }
        ),
    )
    fee = forms.DecimalField(
        required=True,
        validators=[
            MinValueValidator(0, "La cuota real debe ser mayor que 0."),
            MaxValueValidator(50000, "La cuota real debe ser menor a 50000."),
        ],
    )

class CambioDeGrupoForm(forms.Form):
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.none(),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "hx-target": "#change-modal-info",
                "hx-get": reverse_lazy("clases:load-group"),
            }
        )
    )


class BajaForm(forms.Form):
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
             "nombre",
                  "apellido",
                  "dni",
                  "email",
                  "telefono",
                  "direccion",
                  "sexo",
                  "emergency_contact",
                  "fecha_nacimiento"
                  ]

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700",
            }
        )
    )
    def __init__(self, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        self.fields["nombre"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Nombre"}
        )
        self.fields["apellido"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Apellido"}
        )
        self.fields["dni"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Cédula"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Email"}
        )
        self.fields["telefono"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Teléfono"}
        )
        self.fields["emergency_contact"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Contacto de emergencia"}
        )
        self.fields["direccion"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Dirección"}
        )
        self.fields["fecha_nacimiento"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Fecha de nacimiento"}
        )
        self.fields["sexo"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Sexo"}
        )
        if self.initial:
            print(f"initial: {self.initial['fecha_nacimiento']}")
            self.initial["fecha_nacimiento"] = self.initial["fecha_nacimiento"].strftime("%Y-%m-%d")
            self.fields["fecha_nacimiento"].widget.attrs.update(
                {
                    "class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"
                }
            )

    def clean(self) -> Any:
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if email:
            if Alumno.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Ya existe un estudiante con ese email")
        dni = cleaned_data.get("dni")
        if dni:
            if Alumno.objects.filter(dni=dni).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Ya existe un estudiante con esa Cedula")
        return cleaned_data