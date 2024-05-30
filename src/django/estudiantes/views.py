from profiles.models import Alumno
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


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
    success_url = reverse_lazy('students')
    template_name = 'estudiantes/estudiante_form.html'

class AlumnoDeleteView(LoginRequiredMixin,DeleteView):
    model = Alumno
    success_url = reverse_lazy ('students')
    template_name = 'estudiantes/estudiante_confirm_delete.html'
    
class InscripcionNueva(View):
    form_class = None
    template_name = 'estudiantes/inscripcion.html'
    
    def get (self, request, *args, **kwargs):
        return render (request, self.template_name)
    
    def post (self, request, *args, **kwargs):
        pass