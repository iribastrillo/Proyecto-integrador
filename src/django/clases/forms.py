from datetime import datetime
from django import forms
from domain.models import Curso, Salon, Profesor, Dia, Grupo, BloqueDeClase


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = [
            "id",
            "curso",
            "profesores",
            "cupo",
            "fecha_inicio",
            "fecha_baja",
            "activo",
        ]

    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        widget=forms.Select(
            attrs={"hx-get": "cargar-profesores/", "hx-target": "#id_profesores"}
        ),
    )
    profesores = forms.ModelMultipleChoiceField(queryset=Profesor.objects.none())
    cupo = forms.IntegerField(min_value=0, max_value=500)
    fecha_inicio = forms.DateTimeField(widget=forms.DateInput(attrs={"type": "date"}))
    fecha_baja = forms.DateTimeField(
        widget=forms.DateInput(attrs={"type": "date", "hidden": "hidden"}),
        required=False,
        label="",
    )
    activo = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)
        self.fields["curso"].widget.attrs.update(
            {"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700 "}
        )
        self.fields["profesores"].widget.attrs.update(
            {"class": "bg-gray-900    shadow dark:bg-gray-700"}
        )
        self.fields["cupo"].widget.attrs.update(
            {
                "class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700",
                "min": "0",
                "max": "500",
            }
        )
        self.fields["fecha_inicio"].widget.attrs.update(
            {"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"}
        )
        self.fields["fecha_baja"].widget.attrs.update(
            {"class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"}
        )
        if "fecha_inicio" in self.initial:
            self.initial["fecha_inicio"] = self.initial["fecha_inicio"].strftime(
                "%Y-%m-%d"
            )

        if "curso" in self.data:
            curso_id = int(self.data.get("curso"))
            self.fields["profesores"].queryset = Profesor.objects.filter(
                cursos__id=curso_id
            ).order_by("nombre")
        elif self.initial and "curso" in self.initial:
            print(f"THERE IS AN INITIAL VALUE:  {self.initial} ")
            # curso_id = self.initial['curso'].id
            curso_id = self.initial["curso"]

            self.fields["profesores"].queryset = Profesor.objects.filter(
                cursos__id=curso_id
            ).order_by("nombre")

        if self.instance.id is not None:
            self.fields["fecha_baja"] = forms.DateTimeField(
                widget=forms.DateInput(attrs={"type": "date"}), required=False
            )
            self.fields["fecha_baja"].widget.attrs.update(
                {
                    "class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"
                }
            )
            if "fecha_baja" in self.initial and self.initial["fecha_baja"] is not None:
                self.initial["fecha_baja"] = self.initial["fecha_baja"].strftime(
                    "%Y-%m-%d"
                )


class BloqueDeClaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BloqueDeClaseForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.initial["hora_inicio"] = self.initial["hora_inicio"].strftime("%H:%M")
            self.initial["hora_fin"] = self.initial["hora_fin"].strftime("%H:%M")

            self.fields["id"] = forms.CharField(
                widget=forms.HiddenInput(), initial=self.initial["id"]
            )
            print(f"bloque_Clase_id {self.initial['id']}")
            # self.fields["dia"].initial = self.initial['dia']
            self.fields["dia"] = forms.ModelMultipleChoiceField(
                queryset=Dia.objects.all(),
                widget=forms.CheckboxSelectMultiple(
                    attrs={
                        "class": "bg-gray-900   shadow dark:bg-gray-900",
                        "hx-trigger": "change",
                        "hx-include": "[name='salon'],[name='hora_inicio'],[name='hora_fin'],[name='dia'],[name='id'],input[type='checkbox']:checked",
                        "hx-get": f"/app/clases/grupos/{self.initial['id']}/cargar-horas-disponibles/",
                        "hx-target": "#id_hora_inicio",
                        "hx-select-oob": "#id_hora_fin",
                    }
                ),
                initial=self.initial["dia"],
                required=True,
            )
            self.fields["salon"] = forms.ModelChoiceField(
                queryset=Salon.objects.all(),
                widget=forms.Select(
                    attrs={
                        "class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-900",
                        "hx-get": f"/app/clases/grupos/{self.initial['id']}/cargar-horas-disponibles/",
                        "hx-target": "#id_hora_inicio",
                        "hx-select-oob": "#id_hora_fin",
                        "hx-include": "[name='dia'],[name='salon'],[name='hora_inicio'],[name='hora_fin'],[name='id']",
                    }
                ),
                initial=self.initial["salon"],
                required=True,
            )

    class Meta:
        model = BloqueDeClase
        fields = ["dia", "hora_inicio", "hora_fin", "salon", "id"]

    dia = forms.ModelMultipleChoiceField(
        queryset=Dia.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "bg-gray-900   shadow dark:bg-gray-900",
                "hx-trigger": "change",
                "hx-include": "[name='salon'],[name='hora_inicio'],[name='hora_fin'],[name='dia'],[name='id'],input[type='checkbox']:checked",
                "hx-get": "cargar-horas-disponibles/",
                "hx-target": "#id_hora_inicio",
                "hx-select-oob": "#id_hora_fin",
            }
        ),
        required=True,
    )
    hora_inicio = forms.ChoiceField(
        choices=[
            (f"{i//2:02d}:{i%2*30:02d}", f"{i//2:02d}:{i%2*30:02d}") for i in range(48)
        ],
        widget=forms.Select(
            attrs={
                "class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700",
                "id": "id_hora_inicio",
            }
        ),
        required=True,
    )
    hora_fin = forms.ChoiceField(
        choices=[
            (f"{i//2:02d}:{i%2*30:02d}", f"{i//2:02d}:{i%2*30:02d}") for i in range(48)
        ],
        widget=forms.Select(
            attrs={
                "class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700",
                "id": "id_hora_fin",
            }
        ),
        required=True,
    )
    salon = forms.ModelChoiceField(
        queryset=Salon.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-900",
                "hx-get": "cargar-horas-disponibles/",
                "hx-target": "#id_hora_inicio",
                "hx-select-oob": "#id_hora_fin",
                "hx-include": "[name='dia'],[name='salon'],[name='hora_inicio'],[name='hora_fin'],[name='id']",
            }
        ),
        required=True,
    )
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
            raise forms.ValidationError(
                "La hora de fin debe ser mayor a la hora de inicio"
            )
        if dias is None:
            raise forms.ValidationError("Debe seleccionar al menos un día")
        try:
            bloques_ya_ocupados = BloqueDeClase.objects.filter(
                dia__in=dias,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
                salon=salon,
            )
            bloque_ya_ocupado = any(
                bloque.id != self.instance.id for bloque in bloques_ya_ocupados
            )
            if bloque_ya_ocupado:
                raise forms.ValidationError(
                    "Ya existe una clase creada para el salón y el horario seleccionado."
                )

        except BloqueDeClase.DoesNotExist:
            # No existe un bloque con los mismos datos, por lo que no hay problema
            pass

        return cleaned_data
