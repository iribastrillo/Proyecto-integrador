from django.urls import path,include

from . import views

urlpatterns = [
    path('crear-curso/', views.createCourse.as_view(), name='create-course'),
]