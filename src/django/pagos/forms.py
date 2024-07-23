from django import forms
from django.core.exceptions import ValidationError
from domain.models import Pago, Alumno,AlumnoCurso,Curso

class PagoForm(forms.ModelForm):
    alumno = forms.SlugField()
    print(f"Pago Form")

    class Meta:
        model = Pago
        fields = ['monto','descripcion', 'comprobante','curso']
        exclude = ['alumno','fecha']

    def clean_monto(self):
        monto = self.cleaned_data['monto']
        if monto <= 0:
            raise ValidationError('El monto debe ser mayor a $0.00')

        return monto

    def __init__(self, *args, **kwargs):
        if initial := kwargs.get('initial'):
            if 'student_slug' in initial:
                student_slug = initial['student_slug']
                super(PagoForm, self).__init__(*args, **kwargs)
                if student_slug:
                    student = Alumno.objects.get(slug=student_slug)
                    self.fields['alumno'].widget = forms.HiddenInput(attrs={'value': student.slug})
                    enrolled_courses = AlumnoCurso.objects.filter(alumno=student).values_list('curso__pk','curso__nombre')
                    self.fields['curso'] = forms.ChoiceField(choices=enrolled_courses, widget=forms.Select(attrs={'class': 'form-control'}))


        if kwargs.get('instance'):
            if kwargs['instance'].alumno:
                student_slug = kwargs['instance'].alumno.slug
                super(PagoForm, self).__init__(*args, **kwargs)
                if student_slug:
                    student = Alumno.objects.get(slug=student_slug)
                    self.fields['alumno'].widget = forms.HiddenInput(attrs={'value': student.slug})
                    enrolled_courses = AlumnoCurso.objects.filter(alumno=student).values_list('curso__pk','curso__nombre')
                    self.fields['curso'] = forms.ChoiceField(choices=enrolled_courses, widget=forms.Select(attrs={'class': 'form-control'}))



    def clean_alumno(self):
        slug = self.cleaned_data['alumno']
        try:
            alumno=Alumno.objects.get(slug=slug)
            return Alumno.objects.get(slug=slug)
        except Alumno.DoesNotExist:
            raise ValidationError('No existe alumno')
    def clean_curso(self):
        curso_id = self.cleaned_data['curso']
        try:
            curso=Curso.objects.get(pk=curso_id)
            return curso
        except Curso.DoesNotExist:
            raise ValidationError('No existe curso')

    def save(self, commit=True):
        instance = super(PagoForm, self).save(commit=False)
        instance.alumno = self.cleaned_data['alumno']
        if commit:
            instance.save()
        return instance