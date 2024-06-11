from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import InscripcionForm, BajaForm
from profiles.models import Alumno


class AlumnoCreateView(LoginRequiredMixin,CreateView):
    model=Alumno
    fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'direccion', 'telefono','email']
    template_name = 'estudiantes/estudiante_form.html'
    
    def get_success_url(self):
           return reverse_lazy("estudiantes:detail-student", kwargs={"pk": self.get_object().pk})

class AlumnoListView(LoginRequiredMixin,ListView):
    model = Alumno
    template_name = 'estudiantes/estudiante_list.html'

class AlumnoDetailView(LoginRequiredMixin,DetailView):
    model = Alumno
    context_object_name = 'student'
    template_name = 'estudiantes/estudiante_detail.html'

class AlumnoUpdateView(LoginRequiredMixin,UpdateView):
    model = Alumno
    fields = '__all__'
    template_name = 'estudiantes/estudiante_form.html'
    def get_success_url(self) -> str:
        return reverse_lazy ("estudiantes:detail-student", kwargs={'pk': self.get_object().pk})

class AlumnoDeleteView(LoginRequiredMixin,DeleteView):
    model = Alumno
    success_url = reverse_lazy ('students')
    template_name = 'estudiantes/estudiante_confirm_delete.html'
    
class InscripcionNueva(View):
    form_class = InscripcionForm
    template_name = 'estudiantes/partials/enrolment_form.html'
    
    def get (self, request, *args, **kwargs):
        form = self.form_class()
        student = Alumno.objects.get (pk = kwargs['pk'])
        context = {
            'form': form,
            'student': student
        }
        return render (request, self.template_name, context)
    
    def post (self, request, *args, **kwargs):
        form = InscripcionForm (request.POST)    
        student = Alumno.objects.get(pk=kwargs["pk"])    
        if form.is_valid():
            grupo = form.cleaned_data["grupo"]
            if grupo.alumnos.filter(pk=student.pk).exists():
                messages.add_message (request, messages.ERROR, "El estudiante ya está inscripto en ese grupo.")
                return HttpResponseRedirect(reverse('estudiantes:detail-student', kwargs={'pk':student.pk}))
            else:
                grupo.alumnos.add (student)
                grupo.save()
                messages.add_message (request, messages.SUCCESS, f"Inscribiste a {student.apellido}, {student.nombre} en el grupo.")
                return HttpResponseRedirect(reverse('estudiantes:detail-student', kwargs={'pk':student.pk}))
        else:
            messages.add_message (request, messages.ERROR, "El cupo del grupo ya está completo.")
            return HttpResponseRedirect(reverse('estudiantes:detail-student', kwargs={'pk':student.pk}))
        
class BajaEstudiante(View):
    template_name = 'estudiantes/partials/resign_form.html'
    
    def get (self, request, *args, **kwargs):     
        student = Alumno.objects.get (pk = kwargs['pk'])
        form = BajaForm()
        form.fields["grupo"].choices = ((grupo.pk, grupo) for grupo in student.grupo_set.all())
        context = {
            'form': form,
            'student': student
        }
        return render (request, self.template_name, context)
    
    def post (self, request, *args, **kwargs):
        form = BajaForm (request.POST)    
        student = Alumno.objects.get(pk=kwargs["pk"])    
        if form.is_valid():
            grupo = form.cleaned_data["grupo"]
            grupo.alumnos.remove (student)
            grupo.save()
            messages.add_message (request, messages.SUCCESS, f"Bajaste a {student.apellido}, {student.nombre} del grupo.")
            return HttpResponseRedirect(reverse('estudiantes:detail-student', kwargs={'pk':student.pk}))
        else:
            messages.add_message (request, messages.ERROR, "Parece que hubo un problema.")
            return HttpResponseRedirect(reverse('estudiantes:detail-student', kwargs={'pk':student.pk}))