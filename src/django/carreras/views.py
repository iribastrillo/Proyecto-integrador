from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from domain.models import Curso

# Create your views here.
class createCourse (LoginRequiredMixin, CreateView):
    model = Curso
    fields = ['nombre', 'descripcion', 'duracion_meses', 'costo', 'fecha_inicio', 'fecha_fin']