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

from .forms import InscripcionForm, BajaForm
from profiles.models import Alumno
from domain.models import AlumnoCurso

from core.domain.services import calculate_actual_fee


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
        context["groups"] = context["object"].grupo_set.all()        
        context["enrolments"] = AlumnoCurso.objects.filter(alumno=context["object"])
        context["actual_fee"] = calculate_actual_fee (context["enrolments"])
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
        "emergency_contact"
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
        student = Alumno.objects.get(slug=kwargs["slug"])
        context = {"form": form, "student": student}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = InscripcionForm(request.POST)
        student = Alumno.objects.get(slug=kwargs["slug"])
        if form.is_valid():
            grupo = form.cleaned_data["grupo"]
            fee = form.cleaned_data["fee"]
            if grupo.alumnos.filter(slug=student.slug).exists():
                messages.add_message(
                    request,
                    messages.ERROR,
                    "El estudiante ya está inscripto en ese grupo.",
                )
                return HttpResponseRedirect(
                    reverse("estudiantes:detail-student", kwargs={"slug": student.slug})
                )
            else:
                grupo.alumnos.add(student)
                grupo.save()
                AlumnoCurso.objects.create(alumno=student, curso=grupo.curso, fee=fee)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"Inscribiste a {student.apellido}, {student.nombre} en el grupo.",
                )
                return HttpResponseRedirect(
                    reverse("estudiantes:detail-student", kwargs={"slug": student.slug})
                )
        else:
            messages.add_message(
                request, messages.ERROR, "El cupo del grupo ya está completo."
            )
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
        student = Alumno.objects.get(slug=kwargs["slug"])
        if form.is_valid():
            grupo = form.cleaned_data["grupo"]
            grupo.alumnos.remove(student)
            grupo.save()
            inscripcion = AlumnoCurso.objects.filter(alumno=student, curso=grupo.curso)
            inscripcion.delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Bajaste a {student.apellido}, {student.nombre} del grupo.",
            )
            return HttpResponseRedirect(
                reverse("estudiantes:detail-student", kwargs={"slug": student.slug})
            )
        else:
            messages.add_message(
                request, messages.ERROR, "Parece que hubo un problema."
            )
            return HttpResponseRedirect(
                reverse("estudiantes:detail-student", kwargs={"slug": student.slug})
            )


class InhabilitarAlumno(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        student = Alumno.objects.get(slug=kwargs["slug"])
        student.user.is_active = False
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Inhabilitaste el usuario de {student.apellido}, {student.nombre}.",
        )
        return HttpResponseRedirect(
            reverse("estudiantes:detail-student", kwargs={"slug": student.slug})
        )