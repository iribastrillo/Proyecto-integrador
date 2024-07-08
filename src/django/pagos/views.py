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
        form = self.form_class(student_slug=student.slug)

        context = {
            'form': form,
            'student': student

        }
        return render (request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        student = Alumno.objects.get(slug=kwargs['slug'])
        form = self.form_class(request.POST, request.FILES, student_slug=student.slug)
        print(f"student slug{student.slug}")
        if form.is_valid():
            pago = form.save(commit=False)
            pago.alumno = student
            pago.save()
            # Redirect to a success page or render the form again with a success message
            return redirect('estudiantes:detail-student', slug=student.slug)

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
    template_name = 'pagos/pago_list.html'
    context_object_name='lista_pagos'

    def get (self, request, *args, **kwargs):
        print("listando pagos")
        print(self.kwargs)
        student = Alumno.objects.get(slug = kwargs['slug'])
        print(f"Alumno {student.nombre}")
        print(f"Slug {student.slug}")
        pagos= Pago.objects.filter(alumno=student)
        print(f"Pagos {pagos}")

        context = {
            'payment_list': pagos,
            'student': student,
        }
        return render(request, self.template_name, context)


class DetailPago(LoginRequiredMixin, DetailView):
    model = Pago
    template_name = 'pagos/pago_detail.html'
    def get (self, request, *args, **kwargs):
        print("Detalle de pago")
        print(self.kwargs)
        pago = get_object_or_404(Pago, id=kwargs['pago_id'])
        student = pago.alumno
        print(f"Alumno {student.nombre}")
        print(f"Slug {student.slug}")
        pagos= Pago.objects.filter(alumno=student)
        print(f"Pagos {pagos}")

        context = {
            'pago':pago,
            'student_slug': student.slug,
        }
        return render(request, self.template_name, context)


class DeletePago(LoginRequiredMixin, DeleteView):
    # model = Pago
    # template_name = 'pagos/pago_confirm_delete.html'
    # success_url=reverse_lazy('pagos:payments')
    # def get(self, request, *args, **kwargs):
    #     pago = get_object_or_404(Pago, id=kwargs['pk'])
    #     student = pago.alumno
    #     print(f"Eliminando pago for alumno {student.nombre}")
    #     context = {
    #         'pago':pago,
    #         'student_slug': student.slug,
    #     }
    #     return render(request, self.template_name, context)

    # def get_success_url(self) -> str:
    #     return super().get_success_url(f'pagos:payments {student.slug}')
    model = Pago
    template_name = 'pagos/pago_confirm_delete.html'

    def get_object(self, queryset=None):
        # Retrieve the Pago instance being deleted
        return get_object_or_404(Pago, id=self.kwargs['pk'])

    def get_success_url(self):
        # Get the student associated with the Pago instance
        student = self.object.alumno
        # Generate the success URL with the student slug
        return reverse_lazy('pagos:payments', kwargs={'slug': student.slug})

class UpdatePago(LoginRequiredMixin, UpdateView):
    # model=Pago
    # form_class = PagoForm
    # template_name = 'pagos/pago_form.html'
    # success_url=reverse_lazy('pagos:list-pagos')
    def get(self, request, *args, **kwargs):
        print("modificando pago")

        print(self.kwargs)
        pago = get_object_or_404(Pago, id=kwargs['pk'])
        student = pago.alumno
        return render(request, self.template_name, {'form': self.form_class, 'student': student,'form':pago})
    model = Pago
    form_class = PagoForm
    template_name = 'pagos/pago_form.html'

    def get_object(self, queryset=None):
        # Retrieve the Pago instance being edited
        return get_object_or_404(Pago, id=self.kwargs['pk'])

    # def get_form(self, form_class=None):
    #     # Initialize the form with the existing Pago instance data
    #     form = super().get_form(form_class)
    #     form.instance = self.object
    #     student = self.object.alumno
    #     print(student.slug)
    #     form.initial['student'] = student  # Assuming 'alumno' is the field name in your form
    #     print(f"form{form}")
    #     return form

    def get_success_url(self):
        # Get the student associated with the Pago instance
        student = self.object.alumno
        # Generate the success URL with the student slug
        return reverse_lazy('pagos:payments', kwargs={'slug': student.slug})


