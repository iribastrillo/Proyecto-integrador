from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from domain.models import BloqueDeClase, Grupo, Profesor
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CreateGroupForm, BloqueDeClaseForm
from datetime import datetime, timedelta
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class ListBloqueDeClases(LoginRequiredMixin, ListView):
    model = BloqueDeClase
    template_name = "clases/clases_list.html"
    context_object_name = "lista_clases"


class DetailBloqueDeClase(LoginRequiredMixin, DetailView):
    model = BloqueDeClase
    template_name = "clases/clases_list.html"


class DeleteBloqueDeClase(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = BloqueDeClase
    template_name = "clases/clases_confirm_delete.html"
    success_message = "El grupo se eliminó con éxito"

    def get_success_url(self):
        return reverse("clases:detail-group", kwargs={"pk": self.get_object().grupo.pk})

    def get_context_data(self, **kwargs):
        context = super(DeleteBloqueDeClase, self).get_context_data(**kwargs)
        bloque_de_clase = self.get_object()
        context["bloque"] = bloque_de_clase
        context["grupo_pk"] = bloque_de_clase.grupo.pk
        return context


@login_required
def delete_group(request, pk):
    grupo = get_object_or_404(Grupo, id=pk)
    if request.method == "POST":
        grupo.delete()
        return redirect(reverse_lazy("clases:list-groups"))
    return render(request, "clases/grupo_confirm_delete.html", {"grupo": grupo})


def list_groups(request):
    grupos = Grupo.objects.all()
    return render(request, "clases/grupo_list.html", {"lista_grupos": grupos})


# se agrego pk del grupo en caso que sea un update de profesor
## de grupo, para que pueda llegar aca la request y filtrar profesores
## por curso
def load_professors(request, pk=None):
    curso_id = request.GET.get("curso")
    profesores = Profesor.objects.filter(cursos__id=curso_id)
    return render(request, "clases/profesores_options.html", {"profesores": profesores})


def load_group(request):
    id_grupo = request.GET.get("grupo")
    grupo = Grupo.objects.get(pk=id_grupo)
    return render(
        request, "clases/partials/info_grupo_enrolment_modal.html", {"grupo": grupo}
    )


def load_available_hours(request, pk=None):
    selected_days = []
    selected_salon = []
    selected_hours = []
    all_time_slots = []
    bloque_id = None
    start_time = datetime.strptime("00:00", "%H:%M")  # Start at midnight (00:00)
    end_time = datetime.strptime("23:59", "%H:%M")  # End just before midnight (23:59)
    while start_time <= end_time:
        all_time_slots.append(start_time)
        start_time += timedelta(minutes=30)
    simple_time_slots = [slot.strftime("%H:%M") for slot in all_time_slots]
    horas_para_dropdown = simple_time_slots
    horas_para_dropdown = {
        hour: "bloque-available bg-gray-900" for hour in simple_time_slots
    }
    if "id" in request.GET and request.GET.get("id") != "":
        bloque_id = request.GET.get("id")
        selected_hours.append(
            BloqueDeClase.objects.get(pk=bloque_id).hora_inicio.strftime("%H:%M")
        )
        selected_hours.append(
            BloqueDeClase.objects.get(pk=bloque_id).hora_fin.strftime("%H:%M")
        )
    if "salon" in request.GET and request.GET.get("salon") != "":
        selected_salon = request.GET.getlist("salon")
        if "dia" in request.GET:
            selected_days = request.GET.getlist("dia")
        horas_no_disponibles = []
        bloques = BloqueDeClase.objects.filter(salon__id=selected_salon[0])
        selected_days = [int(day) for day in selected_days]
        q_objects = Q()
        for day_id in selected_days:
            q_objects |= Q(dia__id=day_id)
        bloques = bloques.filter(q_objects)
        if bloques:
            horas_no_disponibles.extend(
                [
                    (
                        bloque.hora_inicio.strftime("%H:%M"),
                        bloque.hora_fin.strftime("%H:%M"),
                    )
                    for bloque in bloques
                ]
            )
            all_intervals = set()
            for start, end in horas_no_disponibles:
                intervals = get_minutes_in_range(start, end)
                all_intervals.update(intervals)

            horas_no_disponibles_formateadas = []
            for minutes in sorted(all_intervals):
                hours, mins = divmod(minutes, 60)
                formatted_hour = f"{hours:02}:{mins:02}"
                horas_no_disponibles_formateadas.append(formatted_hour)

            horas_para_dropdown = {
                hour: "bloque-available bg-gray-900"
                if hour not in horas_no_disponibles_formateadas
                else "bloque-taken"
                for hour in simple_time_slots
            }
    horas_para_dropdown.update(
        {hour: "selected" for hour in horas_para_dropdown if hour in selected_hours}
    )
    return render(
        request,
        "clases/horas_options.html",
        {"horas_para_dropdown": horas_para_dropdown},
    )


def convert_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes


def get_minutes_in_range(start_time, end_time):
    start_minutes = convert_to_minutes(start_time)
    end_minutes = convert_to_minutes(end_time)
    return list(range(start_minutes, end_minutes + 1, 30))


class CreateGrupo(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Grupo
    form_class = CreateGroupForm
    template_name = "clases/grupo_form.html"
    success_message = "Se agregó grupo con éxito"

    def get_success_url(self):
        return reverse_lazy("clases:detail-group", kwargs={"pk": self.object.group.pk})

    def form_valid(self, form):
        curso = form.cleaned_data["curso"]
        profesores = form.cleaned_data["profesores"]
        cupo = form.cleaned_data["cupo"]
        grupo = Grupo(curso=curso, cupo=cupo)
        grupo.save()
        grupo.profesores.set(profesores)
        return redirect("clases:detail-group", pk=grupo.pk)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})


class UpdateGrupo(LoginRequiredMixin, UpdateView):
    model = Grupo
    form_class = CreateGroupForm
    template_name = "clases/grupo_form.html"
    success_message = "Se agregó grupo con éxito"

    def get_success_url(self):
        return reverse_lazy("clases:detail-group", kwargs={"pk": self.get_object().pk})


class GrupoDetailView(LoginRequiredMixin, DetailView):
    model = Grupo
    context_object_name = "grupo"
    template_name = "clases/grupo_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupo = self.object
        context["bloques_de_clase"] = BloqueDeClase.objects.filter(grupo=grupo)
        return context


class CreateBloqueDeClase(LoginRequiredMixin, CreateView):
    model_name = BloqueDeClase
    template_name = "clases/partials/bloque_clase_form_partial.html"
    form_class = BloqueDeClaseForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        grupo = Grupo.objects.get(pk=kwargs["pk"])
        context = {"form": form, "grupo": grupo}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = BloqueDeClaseForm(request.POST)
        grupo = Grupo.objects.get(pk=kwargs["pk"])
        if form.is_valid():
            dias = form.cleaned_data["dia"]
            hora_inicio = form.cleaned_data["hora_inicio"]
            hora_fin = form.cleaned_data["hora_fin"]
            salon = form.cleaned_data["salon"]
            bloque = BloqueDeClase.objects.create(
                hora_inicio=hora_inicio, hora_fin=hora_fin, salon=salon, grupo=grupo
            )
            bloque.dia.set(dias)
            bloque.save()
            messages.add_message(request, messages.SUCCESS, f"Clase creada con exito.")
            return HttpResponse()
        else:
            grupo = Grupo.objects.get(pk=self.kwargs["pk"])
            response = render(
                request,
                "clases/partials/bloque_clase_form_partial.html",
                {"form": form, "grupo": grupo},
            )
            response["HX-Retarget"] = "#bloque-clase-modal"
            return response


class BloqueClaseUpdateView(LoginRequiredMixin, UpdateView):
    model = BloqueDeClase
    template_name = "clases/partials/bloque_clase_update_form_partial.html"
    form_class = BloqueDeClaseForm

    def get_context_data(self, **kwargs):
        context = super(BloqueClaseUpdateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        grupo = self.object.grupo
        dias = form.cleaned_data["dia"]
        hora_inicio = form.cleaned_data["hora_inicio"]
        hora_fin = form.cleaned_data["hora_fin"]
        salon = form.cleaned_data["salon"]

        for dia_obj in dias.all():
            try:
                bloque_ya_ocupado = BloqueDeClase.objects.get(
                    dia=dia_obj,
                    hora_inicio__lt=hora_fin,
                    hora_fin__gt=hora_inicio,
                    salon=salon,
                    grupo=grupo,
                )
                if bloque_ya_ocupado != self.object:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        "Ya existe una clase creada para el salon y el horario seleccionado.",
                    )
                    return self.form_invalid(form)
            except BloqueDeClase.DoesNotExist:
                pass
        super().form_valid(form)
        return HttpResponse()

    def get_success_url(self):
        return reverse("clases:detail-group", kwargs={"pk": self.object.grupo.pk})

    def form_invalid(self, form, **kwargs):
        context = super(BloqueClaseUpdateView, self).get_context_data(**kwargs)
        response = render(
            self.request,
            "clases/partials/bloque_clase_update_form_partial.html",
            {"context": context, "form": form, "bloquedeclase": self.object},
        )
        response["HX-Retarget"] = "#bloque-clase-modal"
        return response


def crear_bloque_de_clase(request, pk=None):
    grupo = get_object_or_404(Grupo, pk=pk)

    if request.method == "POST":
        form = BloqueDeClaseForm(request.POST or None)
        if form.is_valid():
            bloque = form.save(commit=False)
            bloque.grupo = grupo
            bloque.save()
            context = {"bloque": bloque}
            return render()
