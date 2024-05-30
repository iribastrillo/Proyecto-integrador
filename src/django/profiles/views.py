from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile (request):
    template = 'profile_detail.html'
    return render (request, template_name=template)