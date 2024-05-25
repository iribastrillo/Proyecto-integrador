from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import (TemplateView,
                                  FormView
                                )

from django.urls import reverse, reverse_lazy
# if we are using success_url (class based views) we have to use reverse_lazy()
# if we are reversing inside a function we can use reverse()
# reverse() returns a string and reverse_lazy() returns an <object>

from domain.forms import ContactForm

def index(request):
    return render(request, reverse_lazy('domanin:home'))


class GraciasView(TemplateView):
    template_name='domain/gracias.html'

class HomeView(TemplateView):
    template_name = 'domain/home.html'


class ContactFormView(FormView):
    form_class=ContactForm
    template_name='domain/contact.html'

    # success url? (NOT a template.html)
    # success_url="/classroom/thank_you/"
    success_url=reverse_lazy('domain:gracias') #this will get the actual url

    # what to do with form?
    def form_valid(self,form):
        print(form.cleaned_data)
        return super().form_valid(form)