from django.shortcuts import render

def home (request):
    template = 'base/home.html'
    return render (request, template_name=template)