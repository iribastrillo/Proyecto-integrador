from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile (request):
    template = 'profiles/profile_detail.html'
    return render (request, template_name=template)