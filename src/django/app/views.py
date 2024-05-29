from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home (request):
    template = 'base/home.html'
    return render (request, template_name=template)