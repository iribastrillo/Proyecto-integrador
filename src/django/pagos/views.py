from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from domain.models import Alumno, Pago
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PagoForm


def create_pago(request: HttpRequest, slug: str) -> HttpResponseRedirect:
    student = Alumno.objects.get(slug=slug)
    if request.method == "POST":
        form = PagoForm(
            request.POST, request.FILES, initial={"student_slug": student.slug}
        )

        if form.is_valid():
            pago = form.save(commit=False)
            pago.alumno = student
            pago.save()
            return HttpResponse()
        else:
            response = render(
                request, "pagos/pago_form.html", {"form": form, "slug": student.slug}
            )
            response["HX-Retarget"] = "#payment-modal"

            return response
    else:
        form = PagoForm(initial={"student_slug": student.slug})
    return render(request, "pagos/pago_form.html", {"form": form, "slug": student.slug})


def update_pago(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    pago = get_object_or_404(Pago, pk=pk)
    student = pago.alumno
    if request.method == "POST":
        form = PagoForm(request.POST, request.FILES, instance=pago)
        if form.is_valid():
            form.save()
            return HttpResponse()
        else:
            response = render(
                request,
                "pagos/update_pago_form.html",
                {"form": form, "pago": pago, "student": student},
            )
            response["HX-Retarget"] = "#payment-modal"
            return response
    else:
        form = PagoForm(instance=pago)
    return render(
        request,
        "pagos/update_pago_form.html",
        {"form": form, "pago": pago, "student": student},
    )


class DeletePago(LoginRequiredMixin, DeleteView):
    model = Pago
    template_name = "pagos/pago_confirm_delete.html"

    def get_success_url(self):
        student = self.kwargs["slug"]
        return reverse_lazy("pagos:payments", kwargs={"slug": student})


class DetailPago(LoginRequiredMixin, DetailView):
    model = Pago
    template_name = "pagos/pago_detail.html"


class ListPagos(LoginRequiredMixin, ListView):
    model = Pago
    template_name = "pagos/pago_list.html"
    context_object_name = "lista_pagos"

    def get(self, request, *args, **kwargs):
        student = Alumno.objects.get(slug=kwargs["slug"])
        pagos = Pago.objects.filter(alumno=student)

        context = {
            "payment_list": pagos,
            "student": student,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        student = Alumno.objects.get(slug=kwargs["slug"])
        pagos = Pago.objects.filter(alumno=student)

        context = {
            "payment_list": pagos,
            "student": student,
        }
        return render(request, self.template_name, context)


class DetailPago(LoginRequiredMixin, DetailView):
    model = Pago
    template_name = "pagos/pago_detail.html"

    def get(self, request, *args, **kwargs):
        pago = get_object_or_404(Pago, id=kwargs["pk"])
        student = pago.alumno

        context = {
            "pago": pago,
            "student_slug": student.slug,
        }
        return render(request, self.template_name, context)


class DeletePago(LoginRequiredMixin, DeleteView):
    model = Pago
    template_name = "pagos/pago_confirm_delete.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Pago, id=self.kwargs["pk"])

    def get_success_url(self):
        student = self.object.alumno
        return reverse_lazy("pagos:payments", kwargs={"slug": student.slug})


class UpdatePago(LoginRequiredMixin, UpdateView):
    model = Pago
    template_name = "pagos/update_form.html"
    fields = ["monto", "descripcion", "comprobante"]

    def post(self, request, *args, **kwargs):
        student = Alumno.objects.get(slug=kwargs["slug"])
        form = self.form_class(request.POST, request.FILES, student_slug=student.slug)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.alumno = student
            pago.save()
            return reverse("pagos:payments", kwargs={"slug": student.slug})

    def get_success_url(self):
        student = self.object.alumno
        return reverse("pagos:payments", kwargs={"slug": student.slug})
