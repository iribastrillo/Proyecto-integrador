from typing import Any
from django.shortcuts import render
from django.utils.timezone import now
# Create your views here.

from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import (
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)

from domain.models import Alumno,Pago

from django.urls import reverse, reverse_lazy

from django.http import HttpRequest, HttpResponse,HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PagoForm

from django.contrib import messages

from django.template.response import TemplateResponse


def create_pago(request: HttpRequest, slug: str) -> HttpResponseRedirect:
    student = Alumno.objects.get(slug=slug)
    if request.method == 'POST':
        form = PagoForm(request.POST, request.FILES, initial={'student_slug': student.slug})

        if form.is_valid():
            pago = form.save(commit=False)
            pago.alumno = student
            pago.save()
            # return HttpResponseRedirect(reverse('pagos:payments', kwargs={'slug': student.slug}))
            return HttpResponse()
        else:
            print(f"form invalid {form.errors}")
            response = render(request, 'pagos/pago_form.html', {'form': form, 'slug': student.slug})
            response['HX-Retarget'] = '#payment-modal'

            return response
            # return TemplateResponse(request, 'pagos/pago_form.html', {'form': form, 'slug': student.slug})
    else:
        form = PagoForm(initial={'student_slug': student.slug})
        # form.initial['fecha'] = now().strftime('%Y-%m-%d')
        print(f"get {student.slug}")
    return render(request, 'pagos/pago_form.html', {'form': form, 'slug': student.slug})


def update_pago(request: HttpRequest,  pk: int) -> HttpResponseRedirect:
    pago = get_object_or_404(Pago, pk=pk)
    student=pago.alumno
    if request.method == 'POST':
        form = PagoForm(request.POST, request.FILES, instance=pago)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(reverse('pagos:payments', kwargs={'slug': student.slug}))
            return HttpResponse()
        else:
            response = render(request, 'pagos/update_pago_form.html', {'form': form, 'pago': pago,'student': student})
            response['HX-Retarget'] = '#payment-modal'
            return response
    else:
        form = PagoForm(instance=pago)
    return render(request, 'pagos/update_pago_form.html', {'form': form, 'pago': pago,'student': student})

class DeletePago(LoginRequiredMixin, DeleteView):
    model = Pago
    template_name = 'pagos/pago_confirm_delete.html'
    def get_success_url(self):
        # Get the student associated with the Pago instance
        student = self.kwargs['slug']
        # Generate the success URL with the student slug
        return reverse_lazy('pagos:payments', kwargs={'slug': student})

class DetailPago(LoginRequiredMixin, DetailView):
    model = Pago
    template_name = 'pagos/pago_detail.html'



class ListPagos(LoginRequiredMixin, ListView):
    model = Pago
    template_name = 'pagos/pago_list.html'
    context_object_name='lista_pagos'

    def get (self, request, *args, **kwargs):
        student = Alumno.objects.get(slug = kwargs['slug'])
        pagos= Pago.objects.filter(alumno=student)

        context = {
            'payment_list': pagos,
            'student': student,
        }
        return render(request, self.template_name, context)

    def post (self, request, *args, **kwargs):
        student = Alumno.objects.get(slug = kwargs['slug'])
        pagos= Pago.objects.filter(alumno=student)

        context = {
            'payment_list': pagos,
            'student': student,
        }
        return render(request, self.template_name, context)


class DetailPago(LoginRequiredMixin, DetailView):
    model = Pago
    template_name = 'pagos/pago_detail.html'
    def get (self, request, *args, **kwargs):
        pago = get_object_or_404(Pago, id=kwargs['pk'])
        student = pago.alumno

        context = {
            'pago':pago,
            'student_slug': student.slug,
        }
        return render(request, self.template_name, context)


class DeletePago(LoginRequiredMixin, DeleteView):
    model = Pago
    template_name = 'pagos/pago_confirm_delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Pago, id=self.kwargs['pk'])

    def get_success_url(self):
        # Get the student associated with the Pago instance
        student = self.object.alumno
        # Generate the success URL with the student slug
        return reverse_lazy('pagos:payments', kwargs={'slug': student.slug})

class UpdatePago(LoginRequiredMixin, UpdateView):

    model = Pago
    # form_class = PagoForm
    template_name = 'pagos/update_form.html'
    fields = [ 'monto','descripcion','comprobante']

    def post(self, request, *args, **kwargs):
        print("Update posts")
        student = Alumno.objects.get(slug=kwargs['slug'])
        form = self.form_class(request.POST, request.FILES, student_slug=student.slug)
        print(f"student slug{student.slug}")
        if form.is_valid():
            print("update form valid")
            pago = form.save(commit=False)
            pago.alumno = student
            pago.save()
            # Redirect to a success page or render the form again with a success message
            return reverse('pagos:payments', kwargs={'slug': student.slug})


    def get_success_url(self):
        student = self.object.alumno
        return reverse('pagos:payments', kwargs={'slug': student.slug})



