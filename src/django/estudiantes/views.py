from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import InscripcionForm
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
    template_name = 'estudiantes/inscripcion.html'
    
    def get (self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form,
        }
        return render (request, self.template_name, context)
    
    def post (self, request, *args, **kwargs):
        form = InscripcionForm (request.POST)        
        if form.is_valid():
            grupo = form.cleaned_data["grupo"]
            alumno = Alumno.objects.get(pk=kwargs["pk"])
            if grupo.alumnos.filter(pk=alumno.pk).exists():
                return redirect("home")
            else:
                grupo.alumnos.add (alumno)
                grupo.save()
                return redirect ("estudiantes:students")
        else:
            return render (request, self.template_name, {'form' : form})