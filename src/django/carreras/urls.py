from django.urls import path,include

from . import views

urlpatterns = [
    path('<pk>/agregar-curso', views.AddCourseToCareer.as_view(), name='add-course'),
    path('crear-curso/', views.CreateCourse.as_view(), name='create-course'),
    path('cursos/', views.ListCourses.as_view(), name='courses'),
    path('crear-carrera/', views.CreateCareer.as_view(), name='create-career'),
    path('', views.ListCareer.as_view(), name='careers'),  
]