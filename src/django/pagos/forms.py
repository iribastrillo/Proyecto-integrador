from django import forms
from django.core.exceptions import ValidationError
from domain.models import Pago, Alumno

class PagoForm(forms.ModelForm):
    alumno = forms.SlugField()
    print(f"Pago Form")

    class Meta:
        model = Pago
        fields = ['monto','descripcion', 'comprobante']
        exclude = ['alumno','fecha']

    def __init__(self, *args, **kwargs):
        if initial := kwargs.get('initial'):
            print(f"initial {initial}")
            if 'student_slug' in initial:
                student_slug = initial['student_slug']
                print(f"student_slug  FORM init {student_slug}")
                super(PagoForm, self).__init__(*args, **kwargs)
                if student_slug:
                    student = Alumno.objects.get(slug=student_slug)
                    print(found_student:=f"found student {student}")
                    self.fields['alumno'].widget = forms.HiddenInput(attrs={'value': student.slug})

        if kwargs.get('instance'):
            print(f"kwargs {kwargs}")
            print(f"student_slug  FORM init {kwargs['instance'].alumno.slug}")
            if kwargs['instance'].alumno:
                student_slug = kwargs['instance'].alumno.slug
                print(  f"student_slug  FORM init {student_slug}")
                super(PagoForm, self).__init__(*args, **kwargs)
                if student_slug:
                    student = Alumno.objects.get(slug=student_slug)
                    self.fields['alumno'].widget = forms.HiddenInput(attrs={'value': student.slug})


    def clean_alumno(self):
        slug = self.cleaned_data['alumno']
        print(f"clean alumno {self}")
        try:
            print(f"finding alumno with slug {slug}")
            alumno=Alumno.objects.get(slug=slug)
            print(f"alumno found {alumno}")
            return Alumno.objects.get(slug=slug)
        except Alumno.DoesNotExist:
            raise ValidationError('No existe alumno')

    def save(self, commit=True):
        instance = super(PagoForm, self).save(commit=False)
        instance.alumno = self.cleaned_data['alumno']
        if commit:
            instance.save()
        return instance
