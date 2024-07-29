import datetime
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from domain.models import Profesor,BloqueDeClase,Dia

from core.domain.services import calculate_payment


class ProfesorCreateView(LoginRequiredMixin, CreateView):
    model = Profesor
    fields = [
        "nombre",
        "apellido",
        "dni",
        "fecha_nacimiento",
        "direccion",
        "telefono",
        "email",
        "sexo",
        "cursos",
    ]
    success_url = reverse_lazy("profiles:users")


class ProfesorListView(LoginRequiredMixin, ListView):
    model = Profesor
    # template_name = 'profesores/listar_profesores.html'
    context_object_name = "lista_profesores"


class ProfesorDetailView(LoginRequiredMixin, DetailView):
    model = Profesor


class ProfesorUpdateView(LoginRequiredMixin, UpdateView):
    model = Profesor
    fields = [
        "nombre",
        "apellido",
        "dni",
        "fecha_nacimiento",
        "direccion",
        "telefono",
        "email",
        "sexo",
        "cursos",
    ]

    def get_success_url(self):
        return reverse_lazy(
            "detail-professor", kwargs={"slug": self.object.user.username}
        )


class ProfesorDeleteView(LoginRequiredMixin, DeleteView):
    model = Profesor
    success_url = reverse_lazy("profiles:users")


class Pagos(View):
    template_name = "profesores/payments.html"

    def get(self, request, *args, **kwargs):
        professor = Profesor.objects.get(slug=kwargs["slug"])
        groups = professor.grupo_set.all()
        iva_included, nominal = calculate_payment(groups)
        context = {
            "professor": professor,
            "monthly_payment": iva_included,
            "nominal": nominal,
            "groups": groups,
        }
        return render(request, self.template_name, context)


def reporte_clases(request,slug):
    profesor=Profesor.objects.get(slug=slug)
    bloques_profesor= BloqueDeClase.objects.filter(grupo__profesores__slug=slug)
    print(f"bloques_profesor: {bloques_profesor}")
    request_salon=request.GET.get("salon")
    request_dias=request.GET.get("dias")
    bloques_por_dia=[]
    if request_salon:
        bloques_profesor=bloques_profesor.filter(salon__id=request_salon)
    if request_dias:
        bloques_profesor=bloques_profesor.filter(dia__id=request_dias)

     # save all the bloques or the bloques most relevant info (bloque Id, hora_inicio,hora_fin,grupo_id_grupo nombre, alumnos, nombres y slugs, salon id, salon nombre) per each day of the week
    for dia in Dia.objects.all():
        bloques_por_dia.append(
            {
                "dia_pk": dia.pk,
                "dia_nombre": dia.name,
                "bloques": bloques_profesor.filter(dia__pk=dia.pk).order_by("hora_inicio"),
            })


    for dia_info in bloques_por_dia:
        for bloque in dia_info["bloques"]:
            if bloque.hora_inicio and bloque.hora_fin:
                print(f"bloque.hora_inicio: {bloque.hora_inicio}")
                print(f"bloque.hora_fin: {bloque.hora_fin}")
                start_row, end_row = calculate_row_indices(bloque.hora_inicio), calculate_row_indices(bloque.hora_fin)
                bloque.start_row = start_row
                bloque.end_row = end_row
                print(f"bloque.start_row: {bloque.start_row}")

    print(f"bloques_por_dia: {bloques_por_dia.__str__()}")


    context={
        'professor':profesor,
        'bloques_profesor':bloques_por_dia,
        'slug':slug,
        # 'calculate_row_indices': calculate_row_indices(),  # Pass the function to the template
        'time_slots': generate_time_slots(),

    }

    return render(request, "profesores/reporte_clases.html",context)




def calculate_row_indices(hora_inicio):
    print(f" calculate row indices hora_inicio: {hora_inicio}")
    # Assuming reference time is 8:00 AM
    reference_time = datetime.datetime.combine(datetime.date.today(), datetime.time(7, 0))
    hora_inicio_datetime = datetime.datetime.combine(datetime.date.today(), hora_inicio)
    time_difference = (hora_inicio_datetime - reference_time).seconds // 60
    return time_difference // 30

def generate_time_slots():
    time_slots = []
    for hour in range(7, 24):
        time_slots.append(f"{hour}:00 AM")
        time_slots.append(f"{hour}:30 AM")
    time_slots.append("12:00 PM")  # Add noon
    return time_slots