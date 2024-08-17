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
from domain.models import AlumnoCurso, Curso, Carrera, Pago, Grupo
from core.domain.services import (
    calculate_total_teacher_spending,
    calculate_total_product_earnings,
    calculate_gains,
    generate_data_enrolments,
    prepare_monthly_addtions_data,
    get_current_month_amount_receivable,
)
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
    enrolments = AlumnoCurso.objects.all()
    payments = Pago.objects.all()
    n_groups = (
        Grupo.objects.annotate(n_alumnos=Count("alumnos"))
        .filter(n_alumnos__gt=0)
        .count()
    )
    total_spending = calculate_total_teacher_spending(Profesor.objects.all())
    total_earnings = calculate_total_product_earnings(payments)
    current_month_amount_receivable = get_current_month_amount_receivable (enrolments)
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
        "payments": payments[:5],
        "careers": Carrera.objects.all(),
        "data": data,
        "monthly_additions": monthly_additions,
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