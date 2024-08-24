from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.db.models.functions import ExtractMonth
from django.db.models import Count, Q
from django.views import View

from profiles.models import Profesor, Alumno
from domain.models import Curso, Carrera, Pago, Grupo
from core.domain.services import (
    calculate_total_teacher_spending,
    calculate_total_product_earnings,
    calculate_gains,
    generate_additions_data,
    generate_dropouts_data,
    generate_monthly_addtions_data,
    generate_monthly_dropouts_data,
    get_current_month_amount_receivable,
)
from core.domain import student_services, product_services
from app.authorization import is_student, is_teacher, is_staff


def home(request):
    if request.user.is_authenticated:            
        if is_staff(request.user):
            return redirect("dashboard")
        if is_student(request.user):
            return HttpResponse("<h1>Entraste como estudiante</h1>")
        if is_teacher(request.user):
            return HttpResponse("<h1>Entraste como profesor</h1>")
    else:
        return redirect ("login")

@user_passes_test(is_staff)
def dashboard(request):
    template = "base/home.html"
    payments = Pago.objects.all()
    enrolments = student_services.students_get_active()
    inactives = student_services.students_get_inactive()
    courses = product_services.products_get_acives()
    n_groups = (
        Grupo.objects.annotate(n_alumnos=Count("alumnos"))
        .filter(n_alumnos__gt=0)
        .count()
    )
    total_spending = calculate_total_teacher_spending(Profesor.objects.all())
    total_earnings = calculate_total_product_earnings(payments)
    current_month_amount_receivable = get_current_month_amount_receivable (enrolments)
    total_gains = calculate_gains(total_earnings, total_spending)
    additions = generate_additions_data(courses)
    dropouts = generate_dropouts_data (courses)
    monthly_additions = generate_monthly_addtions_data(
        enrolments.annotate(month=ExtractMonth("fecha_inscripcion"))
        .values("month")
        .annotate(count=Count("id"))
        .values("month", "count")
    )
    monthly_dropouts = generate_monthly_dropouts_data(
        inactives.annotate(month=ExtractMonth("fecha_baja"))
        .values("month")
        .annotate(count=Count("id"))
        .values("month", "count")
    )
    total_additions = enrolments.count()
    context = {
        "total_spending": total_spending,
        "total_earnings": total_earnings,
        "total_gains": total_gains,
        "courses": courses,
        "payments": payments[:5],
        "careers": Carrera.objects.all(),
        "additions": additions,
        "dropouts": dropouts,
        "monthly_additions": monthly_additions,
        "monthly_dropouts": monthly_dropouts,
        "total_additions": total_additions,
        "n_groups": n_groups,
        "amount_receivable": current_month_amount_receivable
    }
    return render(request, template_name=template, context=context)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/change_password.html"
    success_url = reverse_lazy("profiles:")

    def form_valid(self, form):
        messages.success(self.request, "Cambiaste tu contraseña.")
        return super().form_valid(form)


class Search(View):
    def post(self, request, *args, **kwargs):
        q = request.POST["query"]
        context = {
            "students": Alumno.objects.filter(
                Q(nombre__icontains=q) | Q(apellido__icontains=q)
            ),
            "teachers": Profesor.objects.filter(
                Q(nombre__icontains=q) | Q(apellido__icontains=q)
            ),
            "courses": Curso.objects.filter(nombre__icontains=q),
            "careers": Carrera.objects.filter(nombre__icontains=q),
            "groups": Grupo.objects.filter(curso__nombre__icontains=q),
        }
        return render(
            request, template_name="base/search_results.html", context=context
        )