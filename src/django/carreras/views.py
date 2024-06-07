from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render

from domain.models import Curso, Carrera
from .forms import CreateCareerForm

class CreateCourse (LoginRequiredMixin, CreateView):
    model = Curso
    fields = ['nombre', 'descripcion', 'duracion_meses', 'costo', 'fecha_inicio']
    success_url = reverse_lazy ("careers")
    
class ListCourses (LoginRequiredMixin, ListView):
    model = Curso
    
class DetailCourse(LoginRequiredMixin, DetailView):
    model = Curso
    
class DeleteCourse(LoginRequiredMixin, DeleteView):
    model = Curso
    success_url = reverse_lazy ("courses")
    
class UpdateCourse(LoginRequiredMixin, UpdateView):
    model=Curso
    fields = ['nombre', 'descripcion', 'duracion_meses', 'costo', 'fecha_inicio']
    
class CreateCareer (LoginRequiredMixin, CreateView):
    model = Carrera
    form_class = CreateCareerForm
    
class ListCareer (LoginRequiredMixin, ListView):
    model = Carrera
    
class DetailCareer(LoginRequiredMixin, DetailView):
    model = Carrera
    
class DeleteCareer(LoginRequiredMixin, DeleteView):
    model = Carrera
    
class UpdateCareer(LoginRequiredMixin, UpdateView):
    model = Carrera
    fields = ['nombre', 'descripcion', 'duracion_meses', 'fecha_baja', 'cursos']

class AddCourseToCareer (LoginRequiredMixin, UpdateView):
    model = Carrera
    fields = ['cursos']
    template_name_suffix = '_add_course'

class CoursesAndCareers (LoginRequiredMixin, View):
    template_name = 'carreras/cursos_y_carreras.html'
    
    def get (self, request, *args, **kwargs):
        courses = Curso.objects.all()
        careers = Carrera.objects.all()
        context = {
            'courses': courses,
            'careers': careers,
        }
        return render (request, self.template_name, context)