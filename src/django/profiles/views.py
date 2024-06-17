from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from profesores.views import UpdateView as ProfesorUpdateView
from estudiantes.views import UpdateView as AlumnoUpdateView

from .models import Profesor, Alumno



@login_required
def profile (request):
    template = 'profiles/profile_detail.html'
    return render (request, template_name=template)

class UpdateProfile (LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        professor = request.user.profesor_set.all()
        student = request.user.alumno_set.all()
        if professor.exists():
            pass
        if student.exists():
            pass
        
class ProfessorsAndStudents (LoginRequiredMixin, View):
    template_name = 'profiles/profesores_y_estudiantes.html'
    
    def get (self, request, *args, **kwargs):
        professors = Profesor.objects.all()
        students = Alumno.objects.all()
        context = {
            'professors': professors,
            'students': students,
        }
        return render (request, self.template_name, context)
