from django.views.generic.edit import CreateView 
from django.views.generic.list import ListView 
from django.contrib.auth.mixins import LoginRequiredMixin
from domain.models import Curso, Carrera

# Create your views here.
class createCourse (LoginRequiredMixin, CreateView):
    model = Curso
    fields = ['nombre', 'descripcion', 'duracion_meses', 'costo', 'fecha_inicio', 'fecha_fin']
    
class listCourses (LoginRequiredMixin, ListView):
    model = Curso
    
class createCareer (LoginRequiredMixin, CreateView):
    model = Carrera
    fields = ['nombre', 'descripcion', 'duracion_meses', 'costo', 'fecha_baja', 'fecha_alta', 'cursos']
    
class listCareer (LoginRequiredMixin, ListView):
    model = Carrera
