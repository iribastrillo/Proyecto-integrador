from django.urls import path,include

from . import views

urlpatterns = [
    path('crear-curso/', views.createCourse.as_view(), name='create-course'),
    path('cursos/', views.listCourses.as_view(), name='courses'),
    path('crear-carrera/', views.createCareer.as_view(), name='create-career'),
    path('carreras/', views.listCareer.as_view(), name='careers'),
]