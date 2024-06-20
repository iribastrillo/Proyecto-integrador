from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages

from profiles.models import Alumno, Profesor
from domain.models import AlumnoCurso, Curso, Carrera
from core.domain.services import (
    calculate_total_teacher_spending,
    calculate_total_product_earnings,
    calculate_gains,
    get_students_by_product,
)


@login_required
def dashboard(request):
    template = "base/home.html"
    students_count = Alumno.objects.count()
    students = AlumnoCurso.objects.all()
    total_spending = calculate_total_teacher_spending(Profesor.objects.all())
    total_earnings = calculate_total_product_earnings(students)
    total_gains = calculate_gains(total_earnings, total_spending)
    dummy_data = [
          { "x": "TEO I", "y": 10 },
          { "x": "PRO I", "y": 5 },
          { "x": "INS I", "y": 11 },
          { "x": "TEC I", "y": 2 },
          { "x": "TEO II","y": 2 },
          { "x": "TEC II","y": 5 },
          { "x": "INS II","y": 15 },
        ],
    context = {
        "students_count": students_count,
        "total_spending": total_spending,
        "total_earnings": total_earnings,
        "total_gains": total_gains,
        "courses": Curso.objects.all(),
        "students": students[:5],
        "careers": Carrera.objects.all(),
        "dummy_data": dummy_data
    }
    return render(request, template_name=template, context=context)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/change_password.html"
    success_url = reverse_lazy("profiles:")

    def form_valid(self, form):
        messages.success(self.request, "Cambiaste tu contraseña.")
        return super().form_valid(form)
