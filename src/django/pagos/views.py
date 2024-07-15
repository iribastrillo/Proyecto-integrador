from django.shortcuts import render

# Create your views here.

from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)

from domain.models import Alumno,Pago

from django.urls import reverse, reverse_lazy

from django.http import HttpRequest, HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PagoForm


class CreartePago(LoginRequiredMixin, View):
    print("Agregando Pago")
    form_class = PagoForm
    template_name = 'pagos/pago_form.html'

    def get (self, request, *args, **kwargs):
        student = Alumno.objects.get(slug = kwargs['slug'])
        print(f"Alumno {student.nombre}")
        print(f"Slug {student.slug}")
        form = self.form_class(initial={'alumno': student.nombre}, student_slug=student.slug)

        context = {
            'form': form,
            'student': student
        }
        return render (request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        student = Alumno.objects.get(slug=kwargs['slug'])
        form = self.form_class(request.POST, request.FILES, student_slug=student.slug)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.alumno = student
            pago.save()
            # Redirect to a success page or render the form again with a success message
            return redirect('estudiante:detalle', slug=student.slug)

        else:
            print("form invalid")
            # Form is not valid, render the form again with error messages
            print(form.errors)  # Print the error messages

            context = {
                'form': form,
                'student': student
            }
            return render(request, self.template_name, context)

class ListPagos(LoginRequiredMixin, ListView):
    model = Pago
    template_name = 'pagos/pagos_list.html'
    context_object_name='lista_pagos'

class DetailPago(LoginRequiredMixin, DetailView):
    model = Pago
    template_name = 'pagos/pagos_list.html'

class DeletePago(LoginRequiredMixin, DeleteView):
    model = Pago
    template_name = 'pagos/confirm_delete.html'
    success_url=reverse_lazy('pagos:list-pagos')

class UpdatePago(LoginRequiredMixin, UpdateView):
    model=Pago
    fields = ['alumno', 'monto', 'fecha','descripcion','comprobante']
    template_name = 'pagos/confirm_delete.html'
    success_url=reverse_lazy('pagos:list-pagos')

