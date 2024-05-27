from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView 
from django.contrib.auth.mixins import LoginRequiredMixin
from domain.models import Curso, Carrera

# Create your views here.
class CreateCourse (LoginRequiredMixin, CreateView):
    model = Curso
    fields = ['nombre', 'descripcion', 'duracion_meses', 'costo', 'fecha_inicio', 'fecha_fin']
    
class ListCourses (LoginRequiredMixin, ListView):
    model = Curso
    
class CreateCareer (LoginRequiredMixin, CreateView):
    model = Carrera
    fields = ['nombre', 'descripcion', 'duracion_meses', 'costo', 'fecha_baja', 'fecha_alta', 'cursos']
    
class ListCareer (LoginRequiredMixin, ListView):
    model = Carrera

class AddCourseToCareer (LoginRequiredMixin, UpdateView):
    model = Carrera
    fields = ['cursos']
    template_name_suffix = '_add_course'