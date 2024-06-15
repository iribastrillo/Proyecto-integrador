from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from profesores.views import UpdateView as ProfesorUpdateView
from estudiantes.views import UpdateView as AlumnoUpdateView

from .models import Profesor



@login_required
def profile (request):
    template = 'profiles/profile_detail.html'
    return render (request, template_name=template)

class UpdateProfile (LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        professor = request.user.profesor_set.all()
        student = request.user.alumno_set.all()
        if professor.exists():
            return ProfesorUpdateView.get (self=ProfesorUpdateView().get_queryset(professor.pk), request=request)
        if student.exists():
            return AlumnoUpdateView.get ()
        
