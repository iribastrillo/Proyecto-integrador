from django import forms
from django.core.exceptions import ValidationError
from domain.models import Pago, Alumno, AlumnoCurso, Curso


class PagoForm(forms.ModelForm):
    alumno = forms.SlugField()
    class Meta:
        model = Pago
        fields = ["monto", "fecha", "descripcion", "comprobante", "curso"]
        exclude = ["alumno"]

    fecha = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(PagoForm, self).__init__(*args, **kwargs)
        if initial := kwargs.get("initial"):
            if "student_slug" in initial:
                student_slug = initial["student_slug"]
                if student_slug:
                    student = Alumno.objects.get(slug=student_slug)
                    self.fields["alumno"].widget = forms.HiddenInput(
                        attrs={"value": student.slug}
                    )
                    enrolled_courses = AlumnoCurso.objects.filter(
                        alumno=student
                    ).values_list("curso__pk", "curso__nombre")
                    self.fields["curso"] = forms.ChoiceField(
                        choices=enrolled_courses,
                        widget=forms.Select(attrs={"class": "form-control"}),
                    )
            if "fecha" in self.initial:
                self.initial["fecha"] = self.initial["fecha"].strftime("%Y-%m-%d")
                self.fields["fecha"].widget.attrs.update(
                    {
                        "class": "bg-gray-900 divide-y divide-gray-100  shadow dark:bg-gray-700"
                    }
                )

        if kwargs.get("instance"):
            if kwargs["instance"].alumno:
                student_slug = kwargs["instance"].alumno.slug
                super(PagoForm, self).__init__(*args, **kwargs)
                if student_slug:
                    student = Alumno.objects.get(slug=student_slug)
                    self.fields["alumno"].widget = forms.HiddenInput(
                        attrs={"value": student.slug}
                    )
                    enrolled_courses = AlumnoCurso.objects.filter(
                        alumno=student
                    ).values_list("curso__pk", "curso__nombre")
                    self.fields["curso"] = forms.ChoiceField(
                        choices=enrolled_courses,
                        widget=forms.Select(attrs={"class": "form-control"}),
                    )
            if kwargs["instance"].fecha:
                self.initial["fecha"] = kwargs["instance"].fecha.strftime("%Y-%m-%d")

    def clean_monto(self):
        monto = self.cleaned_data["monto"]
        if monto <= 0:
            raise ValidationError("El monto debe ser mayor a $0.00")

        return monto

    def clean_alumno(self):
        slug = self.cleaned_data["alumno"]
        try:
            alumno = Alumno.objects.get(slug=slug)
            return alumno
        except Alumno.DoesNotExist:
            raise ValidationError("No existe alumno")

    def clean_curso(self):
        curso_id = self.cleaned_data["curso"]
        try:
            curso = Curso.objects.get(pk=curso_id)

            return curso
        except Curso.DoesNotExist:
            raise ValidationError("No existe curso")

    def clean(self):
        cleaned_data = super().clean()
        alumno = cleaned_data.get("alumno")
        curso = cleaned_data.get("curso")
        fecha_pago = cleaned_data.get("fecha")
        mes_actual = fecha_pago.month
        anio_actual = fecha_pago.year

        pago_en_mes_actual = Pago.objects.filter(
            alumno=alumno, curso=curso, fecha__month=mes_actual, fecha__year=anio_actual
        )

        if (
            pago_en_mes_actual.exists()
            and pago_en_mes_actual.first().id != self.instance.id
        ):
            raise forms.ValidationError(
                "El alumno ya ha realizado un pago para este curso en el mes actual."
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super(PagoForm, self).save(commit=False)
        instance.alumno = self.cleaned_data["alumno"]
        if commit:
            instance.save()
        return instance
