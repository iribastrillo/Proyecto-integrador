import datetime
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
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
from django.shortcuts import redirect, render

from .forms import FaltaProfesorForm
from domain.models import Profesor,BloqueDeClase,Dia,FaltaProfesor,Grupo

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = context["object"].grupo_set.all()
        context["monthly_salary"] = calculate_payment (context["groups"])[0]
        return context


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


class FaltaProfesorCreateView(LoginRequiredMixin, CreateView):
    model = FaltaProfesor
    template_name = "profesores/falta_profesor_form.html"
    fields = [
        "profesor_suplente",
        "fecha",
        "grupo",
        "descripcion",
    ]
    def post(self, request: HttpRequest, *args: str, **kwargs: reverse_lazy) -> HttpResponse:
        print("Post")
        print(request.POST)

        return super().post(request, *args, **kwargs)
    # def get(self, request, *args, **kwargs):
    #     professor = Profesor.objects.get(slug=kwargs["slug"])
    #     groups = professor.grupo_set.all()
    #     context = {
    #         "professor": professor,
    #         "groups": groups,
    #         "form": self.form_class,
    #     }
    #     return render(request, self.template_name, context)
    success_url = reverse_lazy( "detail-professor", kwargs={"slug": "2445645"})
    #  return reverse_lazy(
    #         "detail-professor", kwargs={"slug": self.object.user.username}
    #     )

def falta_profesor_create(request: HttpRequest, slug: str) -> HttpResponseRedirect:
    professor=Profesor.objects.get(slug=slug)
    if request.method == 'POST':
        form = FaltaProfesorForm(request.POST)
        print("Post")
        print(request.POST)
        if form.is_valid():
            print(f"Form is valid {form.cleaned_data}")
            profesor_titular_value = form.cleaned_data['profesor_titular']
            print(f"profesor_titular_value: {profesor_titular_value}")
            form.save()
            return redirect('detail-professor', slug=slug)
        else:
            print(f"form invalid {form.errors}")
            response = render(request, 'profesores/falta_profesor_form.html', {'form': form, 'professor': professor})
            response['HX-Retarget'] = '#abscence-modal'

            return response
    else:

        professor = Profesor.objects.get(slug=slug)
        groups = professor.grupo_set.filter(activo=True)
        form = FaltaProfesorForm(initial={"profesor_titular": professor, "grupo": groups})
        context = {
            "form": form,
            "professor": professor,
            "groups": groups,
        }
        return render(request, "profesores/falta_profesor_form.html", context)

def load_professors(request,pk=None):
    print("Loading professors")
    grupo = request.GET.get("grupo")
    print(f"REQYEST {request.GET}")
    curso=Grupo.objects.get(pk=grupo).curso
    profesor_titular_id=request.GET.get("profesor_titular")
    profesores = Profesor.objects.filter(cursos__id=curso.id).exclude(id=profesor_titular_id)
    print(profesores)

    ### ver que se hace en caso de que no haya profesores que den el mismo
    ### curso que el porofesor titular, se podria mostrar un mensaje de error
    ### o simplemente mostrar todos los profesores

    # if profesores is None or profesores.count()==0:
    #     profesores = Profesor.objects.all()
    return render(request, "profesores/profesores_options.html", {"profesores": profesores})


def list_faltas_profesor(request,slug):
    print(f"Listando faltas de {slug}")
    profesor=Profesor.objects.get(slug=slug)
    faltas=FaltaProfesor.objects.filter(profesor_titular=profesor)
    print(f"faltas: {faltas}")
    context={
        'profesor':profesor,
        'faltas':faltas,
    }
    return render(request, "profesores/listar_faltas.html",context)

def detail_falta(request,pk):
    falta=FaltaProfesor.objects.get(pk=pk)
    context={
        'falta':falta,
    }
    return render(request, "profesores/detalle_falta.html",context)

def update_falta(request,pk):
    print(f"Update falta {pk}")
    falta=FaltaProfesor.objects.get(pk=pk)
    if request.method == 'POST':
        form = FaltaProfesorForm(request.POST, instance=falta)
        if form.is_valid():
            form.save()
            return redirect('list-missing-professor', slug=falta.profesor_titular.slug)
    else:
        print(f"Update falta {pk}")

        form = FaltaProfesorForm(instance=falta)
        print(f" update Form: {form}")
    context = {
        'form': form,
        'falta': falta,
        'professor':falta.profesor_titular,
    }
    return render(request, "profesores/falta_profesor_form.html", context)

def delete_falta(request,pk):
    falta=FaltaProfesor.objects.get(pk=pk)
    falta.delete()
    return redirect(request,'list-missing-professor', slug=falta.profesor_titular.slug)


class DeleteFaltaProfesor(LoginRequiredMixin, DeleteView):
    model = FaltaProfesor
    template_name = 'profesores/profesor_falta_confirm_delete.html'
    def get_success_url(self):
        # Get the student associated with the Pago instance
        profesor = self.kwargs['slug']
        # Generate the success URL with the student slug
        return reverse_lazy('list-missing-professor', kwargs={'pk': profesor})

class DetailFaltaProfesor(LoginRequiredMixin, DetailView):
    model = FaltaProfesor
    template_name = 'profesores/detalle_falta.html'