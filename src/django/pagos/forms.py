from django import forms
from django.core.exceptions import ValidationError
from domain.models import Pago, Alumno

class PagoForm(forms.ModelForm):
    alumno = forms.SlugField()
    print(f"Pago Form")

    class Meta:
        model = Pago
        fields = ['alumno', 'monto','descripcion', 'comprobante']

    def __init__(self, *args, **kwargs):
        student_slug = kwargs.pop('student_slug', None)

        super(PagoForm, self).__init__(*args, **kwargs)
        if student_slug:
            student = Alumno.objects.get(slug=student_slug)
            print(student.nombre)
            self.fields['alumno'].initial = student.id
            self.fields['alumno'].widget = forms.HiddenInput()

    def clean_alumno(self):
        slug = self.cleaned_data['alumno']
        try:
            return Alumno.objects.get(slug=slug)
        except Alumno.DoesNotExist:
            raise ValidationError('No existe alumno')

    def save(self, commit=True):
        instance = super(PagoForm, self).save(commit=False)
        instance.alumno = self.cleaned_data['alumno']
        if commit:
            instance.save()
        return instance
