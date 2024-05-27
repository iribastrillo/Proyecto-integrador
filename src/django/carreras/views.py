from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from domain.models import Curso, Carrera


class CreateCourse (LoginRequiredMixin, CreateView):
    model = Curso
    fields = ['nombre', 'descripcion', 'duracion_meses', 'costo', 'fecha_inicio', 'fecha_fin']
    
class ListCourses (LoginRequiredMixin, ListView):
    model = Curso
    
class DetailCourse(LoginRequiredMixin, DetailView):
    model = Curso
    
class DeleteCourse(LoginRequiredMixin, DeleteView):
    model = Curso
    
class UpdateCourse(LoginRequiredMixin, UpdateView):
    model=Curso
    fields = ['nombre', 'descripcion', 'duracion_meses', 'costo', 'fecha_inicio', 'fecha_fin']
    
class CreateCareer (LoginRequiredMixin, CreateView):
    model = Carrera
    fields = ['nombre', 'descripcion', 'duracion_meses', 'costo', 'fecha_baja', 'fecha_alta', 'cursos']
    
class ListCareer (LoginRequiredMixin, ListView):
    model = Carrera
    
class DetailCareer(LoginRequiredMixin, DetailView):
    model = Carrera
    
class DeleteCareer(LoginRequiredMixin, DeleteView):
    model = Carrera
    
class UpdateCareer(LoginRequiredMixin, UpdateView):
    model = Carrera
    fields = ['nombre', 'descripcion', 'duracion_meses', 'costo', 'fecha_baja', 'fecha_alta', 'cursos']

class AddCourseToCareer (LoginRequiredMixin, UpdateView):
    model = Carrera
    fields = ['cursos']
    template_name_suffix = '_add_course'
