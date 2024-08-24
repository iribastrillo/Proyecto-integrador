import datetime
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .forms import InscripcionForm, BajaForm, CambioDeGrupoForm
from profiles.models import Alumno
from domain.models import AlumnoCurso,Grupo

from core.domain.services import calculate_actual_fee
from core.domain import student_services, product_services
from core.domain.exceptions import GroupCompleteException, StudentAlreadyEnroledException, NoAlternativeException, StudentHasEnroledException


class AlumnoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Alumno
    fields = [
        "nombre",
        "apellido",
        "dni",
        "fecha_nacimiento",
        "direccion",
        "telefono",
        "email",
        "sexo",
        "emergency_contact",
    ]
    template_name = "estudiantes/estudiante_form.html"
    success_message = "Se agregó al estudiante con éxito"

    def get_success_url(self):
        return reverse_lazy(
            "estudiantes:detail-student", kwargs={"slug": self.object.user.username}
        )


class AlumnoListView(LoginRequiredMixin, ListView):
    model = Alumno
    template_name = "estudiantes/estudiante_list.html"


class AlumnoDetailView(LoginRequiredMixin, DetailView):
    model = Alumno
    context_object_name = "estudiante"
    template_name = "estudiantes/estudiante_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = student_services.student_get_groups (context["object"])
        context["enrolments"] = student_services.student_get_active_enrolments (context["object"])
        context["actual_fee"] = calculate_actual_fee(context["enrolments"])
        return context


class AlumnoUpdateView(LoginRequiredMixin, UpdateView):
    model = Alumno
    fields = [
        "nombre",
        "apellido",
        "dni",
        "fecha_nacimiento",
        "direccion",
        "telefono",
        "email",
        "sexo",
        "emergency_contact",
    ]
    template_name = "estudiantes/estudiante_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "estudiantes:detail-student", kwargs={"slug": self.get_object().slug}
        )


class AlumnoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Alumno
    context_object_name = "estudiante"
    success_url = reverse_lazy("profiles:users")
    success_message = "El estudiante se eliminó con éxito"
    template_name = "estudiantes/estudiante_confirm_delete.html"


class InscripcionNueva(LoginRequiredMixin, View):
    form_class = InscripcionForm
    template_name = "estudiantes/partials/enrolment_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        student = student_services.student_get_by_slug (kwargs["slug"])
        context = {"form": form, "student": student}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = InscripcionForm(request.POST)
        if form.is_valid():
            student = student_services.student_get_by_slug (kwargs["slug"])
            group = form.cleaned_data["grupo"]
            fee = form.cleaned_data["fee"]
            try:
                student_services.student_enroll(student, group, fee)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"Inscribiste a {student.apellido}, {student.nombre} en el grupo.",
                )
            except GroupCompleteException:
                messages.add_message(
                request, messages.ERROR, "El cupo del grupo ya está completo."
                )
            except StudentAlreadyEnroledException:
                 messages.add_message(
                    request,
                    messages.ERROR,
                    "El estudiante ya está inscripto en ese grupo.",
                )
            except StudentHasEnroledException:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "El estudiante ya tiene una inscripción activa a este producto.",
                )
            finally:
                return HttpResponseRedirect(
                    reverse("estudiantes:detail-student", kwargs={"slug": student.slug})
                )


class BajaEstudiante(LoginRequiredMixin, View):
    template_name = "estudiantes/partials/resign_form.html"

    def get(self, request, *args, **kwargs):
        student = Alumno.objects.get(slug=kwargs["slug"])
        form = BajaForm()
        form.fields["grupo"].choices = (
            (grupo.pk, grupo) for grupo in student.grupo_set.all()
        )
        context = {"form": form, "student": student}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = BajaForm(request.POST)
        if form.is_valid():
            grupo = form.cleaned_data["grupo"]
            student = student_services.student_get_by_slug (kwargs["slug"])
            student_services.student_resign_course (student, grupo)
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Bajaste a {student.apellido}, {student.nombre} del grupo.",
            )
        else:
            messages.add_message(
                request, messages.ERROR, "Parece que hubo un problema."
            )
        return HttpResponseRedirect(
            reverse("estudiantes:detail-student", kwargs={"slug": student.slug})
        )


class InhabilitarAlumno(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        student = Alumno.objects.get(slug=kwargs["slug"])
        groups = Grupo.objects.filter(alumnos=student)
        context = {"student": student, "groups": groups}
        return render(request, "estudiantes/partials/disable_student.html", context)


    def post(self, request, *args, **kwargs):
        student = Alumno.objects.get(slug=kwargs["slug"])
        alumno_curso = AlumnoCurso.objects.filter(alumno=student)
        for ac in alumno_curso:
            ac.fecha_baja = datetime.date.today()
            ac.save()


        student.user.is_active = False
        student.user.save()

        grupo = student.grupo_set.all()
        for g in grupo:
            g.alumnos.remove(student)
            g.save()
        student.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            f"Inhabilitaste el usuario de {student.apellido}, {student.nombre}.",
        )
        return HttpResponseRedirect(
            reverse("estudiantes:detail-student", kwargs={"slug": student.slug})
        )

      
class CambioDeGrupo (LoginRequiredMixin, View):
    form_class = CambioDeGrupoForm
    template_name = "estudiantes/partials/group_change_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        group = product_services.group_get_by_id(kwargs["id"])
        student = student_services.student_get_by_slug (kwargs["slug"])
        try:
            alternatives = product_services.group_get_change_alternatives(group)
            form.fields["grupo"].choices = (
            (grupo.pk, grupo) for grupo in alternatives)
        except NoAlternativeException:
            messages.add_message(
                request, messages.ERROR, "¡Parece que no hay grupo al cual cambiar!"
                )
        context = {"form": form, "student": student, "group": group}
        return render(request, self.template_name, context)
    
    def post (self, request, *args, **kwargs):
        form = BajaForm(request.POST)
        if form.is_valid():
            student = student_services.student_get_by_slug (kwargs["slug"])
            fr = product_services.group_get_by_id(kwargs["id"])
            to = form.cleaned_data["grupo"]
            try:
                student_services.student_change_group(student, fr, to)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"Cambiaste a {student.apellido}, {student.nombre} al grupo {to.identificador}.",
                )
            except GroupCompleteException:
                messages.add_message(
                request, messages.ERROR, "El cupo del grupo ya está completo."
                )
            finally:
                return HttpResponseRedirect(
                    reverse("estudiantes:detail-student", kwargs={"slug": student.slug})
                )
                
            
class HabilitarAlumno(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        student = Alumno.objects.get(slug=kwargs["slug"])
        context = {"student": student}

        return render(request, "estudiantes/partials/disable_student.html", context)


    def post(self, request, *args, **kwargs):
        student = Alumno.objects.get(slug=kwargs["slug"])
        student.user.is_active = True
        student.user.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            f"Habilitaste el usuario de {student.apellido}, {student.nombre}.",
        )
        return HttpResponseRedirect(
            reverse("estudiantes:detail-student", kwargs={"slug": student.slug})
        )
