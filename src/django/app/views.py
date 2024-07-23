from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models.functions import ExtractMonth
from django.db.models import Count

from profiles.models import Profesor
from domain.models import AlumnoCurso, Curso, Carrera, Pago
from core.domain.services import (
    calculate_total_teacher_spending,
    calculate_total_product_earnings,
    calculate_gains,
    generate_data_enrolments,
    prepare_monthly_addtions_data
)


@login_required
def dashboard(request):
    template = "base/home.html"
    enrolments = AlumnoCurso.objects.all()
    total_spending = calculate_total_teacher_spending(Profesor.objects.all())
    total_earnings = calculate_total_product_earnings(Pago.objects.all())
    total_gains = calculate_gains(total_earnings, total_spending)
    data = generate_data_enrolments(Curso.objects.all())
    monthly_additions = prepare_monthly_addtions_data(
        enrolments.annotate(month=ExtractMonth("fecha_inscripcion"))
        .values("month")
        .annotate(count=Count("id"))
        .values("month", "count")
    )
    total_additions = enrolments.count()
    context = {
        "total_spending": total_spending,
        "total_earnings": total_earnings,
        "total_gains": total_gains,
        "courses": Curso.objects.all(),
        "enrolments": enrolments[:5],
        "careers": Carrera.objects.all(),
        "data": data,
        "monthly_additions": monthly_additions,
        "total_additions": total_additions
    }
    return render(request, template_name=template, context=context)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/change_password.html"
    success_url = reverse_lazy("profiles:")

    def form_valid(self, form):
        messages.success(self.request, "Cambiaste tu contraseña.")
        return super().form_valid(form)
