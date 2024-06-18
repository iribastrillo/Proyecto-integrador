from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages


@login_required
def home(request):
    template = "base/home.html"
    return render(request, template_name=template)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/change_password.html"
    success_url = reverse_lazy("profiles:")

    def form_valid(self, form):
        messages.success(self.request, "Cambiaste tu contraseña.")
        return super().form_valid(form)
